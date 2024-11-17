import os
from dotenv import load_dotenv
from models import Listing, Calendar  
from data.data_fetcher import fetch_data
from data.data_preprocessing import read_data, filter_listings_detailed, filter_calendar_detailed
from db_manager import DatabaseManager

def update_db(session):
    """Update db with up-to-date information"""
    try:
        fetch_data(download_directory="downloads")
        listings_detailed, calendar_detailed = read_data()
        listings_filtered = filter_listings_detailed(listings_detailed)
        calendar_filtered = filter_calendar_detailed(calendar_detailed)

        update_listings_table(listings_filtered, session)
        update_calendar_table(calendar_filtered, session)

    except Exception as e:
        print(f"An error occurred while updating the database: {e}")
    finally:
        session.close()

def update_listings_table(listings_filtered, session):
    """Update listings table"""
    try:
        session.query(Listing).delete()
        session.commit()  
        
        session.bulk_insert_mappings(Listing, listings_filtered.to_dict(orient="records"))
        session.commit() 
        
        print("Listings table successfully updated.")
        
    except Exception as update_exception:
        session.rollback() 
        print(f"An error occurred while updating the listings table: {update_exception}")        

def update_calendar_table(calendar_filtered, session):
    """Update calendar table"""
    try:
        session.query(Calendar).delete()
        session.commit()  
        
        session.bulk_insert_mappings(Calendar, calendar_filtered.to_dict(orient="records"))
        session.commit()  
        
        print("Calendar table successfully updated.")
        
    except Exception as update_exception:
        session.rollback()  
        print(f"An error occurred while updating the calendar table: {update_exception}")   

if __name__ == '__main__':
    
    load_dotenv("../.env")  
    db_uri = os.getenv('DB_URI')
    
    database_manager = DatabaseManager()
    database_manager.init_db()
    update_db(session=database_manager.get_session())
