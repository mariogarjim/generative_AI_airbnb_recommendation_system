import os

from assistants.airbnb_assistant import AirbnbAssistant
from data_handler.data_fetcher import download_and_uncompress, inside_airbnb_scrapper
from data_handler.data_processing import handle_data


class AirbnbRecommendator:
    """Airbnb recommendator singleton class"""

    _instance = None

    def __new__(cls):
        """New method for singleton class"""
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Init method"""
        if not hasattr(self, "initialized"):
            self.initialized = True
            self.download_directory = "downloads"
            if not self.__data_exists():
                self.urls = {}
                self.__fetch_data()
            
            self.listings_detailed, self.airbnb_df = handle_data()
            self.airbnb_assistant = AirbnbAssistant()

    def __data_exists(self):
        """Return true if data exist. 
        If data exists, it is not necessary to download it again.
        """
        file_listings = "listings_detailed.csv"
        file_calendar = "calendar_detailed.csv"

        return os.path.isdir(self.download_directory) and \
               os.path.isfile(f"{self.download_directory}/{file_calendar}") and \
               os.path.isfile(f"{self.download_directory}/{file_listings}")
        

    def __fetch_data(self):
        """Fetch the data from the Inside Airbnb site."""
        
        self.urls = inside_airbnb_scrapper()
        if self.urls:
            download_and_uncompress(self.urls, self.download_directory)
        else:
            print("No URLs found to download.")

    def get_recommendation(self, user_query):
        """Get recommendation from airbnb LLM assistant based on user query

        Args:
            user_query (string): User query

        Returns:
            response (dict): LLM recommendation
        """
        self.airbnb_assistant.chat_with_airbnb_assistant(self.airbnb_df, self.listings_detailed, user_query)
        return self.airbnb_assistant.response
