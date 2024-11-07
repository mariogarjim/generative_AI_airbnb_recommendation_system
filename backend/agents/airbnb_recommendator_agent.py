from agents.agent import Agent


class AirbnbRecommendatorAgent(Agent):
    """User context retriever agent.

    Extract relevant context to recommend airbnb from the user
    """

    def __init__(self, airbnb_recommendation) -> None:
        """Airbnb recommendator system"""
        instructions = (
            f"You are an Airbnb recommendator system. Your task is to provide a brief, clear, user-centered \
            of what {airbnb_recommendation.to_string()} is being recommended. If no Airbnb meets the user's criteria, \
            inform the user politely that none of the available listings match their requirements, and recommend him  \
            change to be more flexible with their travel date or destination."
        )
        super().__init__(name="airbnb_recommendator_system", instructions=instructions, tools=[])
    
        