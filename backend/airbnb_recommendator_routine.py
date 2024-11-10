
import openai
import pandas as pd

from agents.airbnb_recommendator_agent import AirbnbRecommendatorAgent
from agents.user_context_retriever_agent import UserContextRetrieverAgent
from data_handler.data_fetcher import fetch_data
from data_handler.data_filter import filter_data
from data_handler.data_preprocessing import handle_data


class AirbnbRecommendatorRoutine:
    """Airbnb recommendator routine singleton class"""
    
    _instance = None

    def __new__(cls):
        """New method for singleton class"""
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, download_directory = "downloads"):
        """_summary_

        Args:
            user_input (str): User input
            download_directory (str, optional): Download directory for data. 
             Defaults to "downloads".
        """
        if not hasattr(self, "initialized"):
            self.initialized = True
            fetch_data(download_directory)
            
            self.airbnb_df, self.listings_detailed = handle_data()
            
            self.messages = []

    def get_completion(self, agent):
        """Get a completion response from the specified agent.

        Args:
            agent (Agent): An instance of the agent class 
        Returns:
            dict: The message from the OpenAI chat completion 
        """
        if len(agent.tool_schemas) > 0:
            response = openai.chat.completions.create(
                model = agent.model,
                messages = [{"role": "system", "content": agent.instructions}] + self.messages,
                tools = agent.tool_schemas,
            )
        else:
            response = openai.chat.completions.create(
                model = agent.model,
                messages = [{"role": "system", "content": agent.instructions}] + self.messages,
            )
        
        print(f"Response message: {response.choices[0].message}")
        
        return response.choices[0].message
    
    def airbnb_recommendation_routine(self, user_message):
        """Run LLM routine
        
        Args:
            user_message (str): User input message
        """
        recommended_airbnb = pd.DataFrame()
        recommended_airbnb_url = ""
        recommended_airbnb_picture = ""
        
        user_request = {"role": "user", "content": user_message}
        self.messages.append(user_request)
        
        # Retrieving user needs
        user_context_retiever_agent = UserContextRetrieverAgent()
        user_context_retiever_response = self.run_full_turn(agent=user_context_retiever_agent)
        print(f"test: {user_context_retiever_response}")
        user_context = user_context_retiever_response["messages"][1]["content"]
        
        # Filtering df by user needs
        filtered_airbnb_df = filter_data(airbnb_df=self.airbnb_df, user_context=user_context)
        
        if len(filtered_airbnb_df) > 0:
            recommended_airbnb = filtered_airbnb_df.iloc[0]
            recommended_airbnb_id = recommended_airbnb["id"]
            recommended_airbnb_url =  self.listings_detailed[self.listings_detailed["id"] 
                                                             == recommended_airbnb_id].iloc[0]["listing_url"]
            recommended_airbnb_picture = self.listings_detailed[self.listings_detailed["id"] 
                                                                == recommended_airbnb_id].iloc[0]["picture_url"]
        else: 
            print("No airbnb avaliable")
        
        # Giving airbnb recommendation to the user
        self.messages.clear()
        self.messages.append(user_request)
        airbnb_recommendator_agent = AirbnbRecommendatorAgent(airbnb_recommendation=recommended_airbnb)
        response = self.run_full_turn(agent=airbnb_recommendator_agent)
        reason_of_recommendation = response["messages"][0].content
        
        return {
                "reason" : reason_of_recommendation,
                "url": recommended_airbnb_url,
                "image_url": recommended_airbnb_picture,
               }
        
        
        
        
        
        
    
        
        
        
    def run_full_turn(self, agent):
        """Run interaction user-agent

        Args:
            agent (Agent): Current agent to interact
            messages (list): History of messages
            
        Returns:
            dict: Current agent and its interaction
        """
        num_init_messages = len(self.messages)        
        
        message = self.get_completion(agent)
        self.messages.append(message)
        
        if not message.tool_calls:
            return {"agent":agent, "messages":self.messages[num_init_messages:]}

        for tool_call in message.tool_calls:
            result = agent.execute_tool_call(tool_call=tool_call, 
                                                tool_mapping=agent.tool_maps, 
                                                agent_name=agent.name)
            result_message = {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            }
            self.messages.append(result_message)
            
        return {"agent":agent, "messages":self.messages[num_init_messages:]}
    