
from datetime import datetime

import pandas as pd

from agents.agent import Agent


class UserContextRetrieverAgent(Agent):
    """User context retriever agent.

    Extract relevant context to recommend airbnb from the user
    """

    def __init__(self) -> None:
        """User context retriever agent constructor"""
        instructions = f"You are a recommendator assistant that retrieves context information from the \
            user's input. Please note that today's date is {datetime.today().strftime('%d-%m-%Y')}. \
            Please infer latitude and longitude based on the user's destination."
        super().__init__(name="context_retriever_agent", instructions=instructions, tools=[self.get_user_context])
    
    def get_user_context(
        self,
        destination: str,
        latitude: float,
        longitude: float,
        travel_date: str = None,
        travelers: int = 1,
        budget: int = None,
    ):
        """Provides relevant context regarding to user travel.

        Parameters:
        - destination (str): Location or destination specified by the user.
        - latitude (float): Latitude of the specified destination.
        - longitude (float): Longitude of the specified destination.
        - travel_date (str, optional): Date of travel in "YYYY-MM-DD" format. 
        If unspecified, defaults to the upcoming weekend.
        - travelers (int, optional): Number of travelers. Defaults to one traveler.
        - budget (float, optional): Maximum budget per night in USD. 
        If unspecified, assume there is no maximum budget.

        Returns:
        - dict: User context
        """
        if not destination:
            return {}

        context = {
            "destination": destination,
            "latitude": latitude,
            "longitude": longitude,
            "travel_date": travel_date,
            "travelers": travelers,
            "budget": budget,
        }
        
        return context
        