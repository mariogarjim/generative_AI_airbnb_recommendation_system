import pandas as pd
from datetime import datetime

def read_data():
    """Read Airbnb data from CSV files.

    Returns:
        tuple: A tuple containing two DataFrames:
            - listings_detailed: DataFrame with detailed listings.
            - calendar_detailed: DataFrame with calendar information.
    """
    listings_detailed = pd.read_csv("downloads/listings_detailed.csv")
    calendar_detailed = pd.read_csv("downloads/calendar_detailed.csv")

    return listings_detailed, calendar_detailed

def filter_listings_detailed(listings_detailed):
    """Filter listings based on specific criteria.

    Args:
        listings_detailed (DataFrame): The detailed listings DataFrame.

    Returns:
        DataFrame: A filtered DataFrame containing only relevant listings.
    """
    columns = [
        "id",
        "name",
        "latitude",
        "longitude",
        "host_acceptance_rate",
        "number_of_reviews",
        "review_scores_rating",
        "accommodates",
        "minimum_nights",
    ]
    
    stored_columns = [
        "id",
        "name",
        "latitude",
        "longitude",
        "accommodates",
        "minimum_nights"
    ]

    filtered_listings = listings_detailed[columns]

    # Maintain only airbnbs with host acceptance > 70%
    filtered_listings = filtered_listings[filtered_listings["host_acceptance_rate"].notna()]
    filtered_listings["host_acceptance_rate_numeric"] = (
        filtered_listings["host_acceptance_rate"].str.rstrip("%").astype(float)
    )
    filtered_listings = filtered_listings[filtered_listings["host_acceptance_rate_numeric"] > 70]
    filtered_listings = filtered_listings.drop(columns=["host_acceptance_rate_numeric"])

    # Maintain only airbnbs with 5 or more reviews
    filtered_listings = filtered_listings[filtered_listings["number_of_reviews"] >= 5]

    # Maintain only airbnbs with review score rating > 3
    filtered_listings = filtered_listings[filtered_listings["review_scores_rating"].notna()]
    filtered_listings = filtered_listings[filtered_listings["review_scores_rating"] >= 3.0]

    # Filter by relevant columns
    filtered_listings = filtered_listings[stored_columns]

    return filtered_listings

def filter_calendar_detailed(calendar_detailed):
    """Filter calendar df

    Args:
        calendar_detailed (DataFrame): The detailed calendar DataFrame.

    Returns:
        DataFrame: A filtered DataFrame containing only relevant calendar cols.
    """
    
    stored_columns = [
        "listing_id",
        "date",
        "price",
    ]
    
    
    # Remove non avaliable dates
    calendar_detailed = calendar_detailed[calendar_detailed["available"] == "t"]
    # Transform date column from str to date
    calendar_detailed.loc[:, "date"] = pd.to_datetime(calendar_detailed["date"], format="%Y-%m-%d").dt.date
    # Transform personalized price column to correct int format
    calendar_detailed.loc[:, "price"] = (calendar_detailed["price"]
                                      .str.replace("$", "", regex=False)
                                      .str.replace(".", "", regex=False)    
                                      .str.replace(",", ".", regex=False)  
                                      .astype(float))  
    
    
    calendar_detailed = calendar_detailed[stored_columns]
    
    return calendar_detailed