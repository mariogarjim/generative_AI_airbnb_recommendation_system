import inspect
import json
import os

import openai
from dotenv import load_dotenv


class Agent:
    """Base class for a LLM asgent."""

    def __init__(self, name, instructions, tools) -> None:
        """Initialize API key."""
        # Load dotenv to retrieve environment variables
        load_dotenv()
        openai.api_key = os.getenv("API_KEY")

        self.name = name
        self.model = "gpt-4o-mini"
        self.temperature = 0.1
        self.instructions = instructions
        self.tools = []
        self.tool_schemas = []
        self.tool_maps = {}
        for tool in tools:
            self.tools.append(tool)
            self.tool_schemas.append(self.function_to_schema(tool))
            self.tool_maps[tool.__name__] = tool

        
    def function_to_schema(self, func) -> dict:  
        """Convert function to LLM schema

        Args:
            func (func): Function

        Returns:
            dict(dict): Dict with func shceme 
        """
        type_map = {
            str: "string",
            int: "integer",
            float: "number",
            bool: "boolean",
            list: "array",
            dict: "object",
            type(None): "null",
        }

        signature = inspect.signature(func)
        
        parameters = {}
        for param in signature.parameters.values():
            
            param_type = type_map.get(param.annotation, "string")
            
            parameters[param.name] = {"type": param_type}

        required = [
            param.name
            for param in signature.parameters.values()
            if param.default == inspect._empty
        ]

        return {
            "type": "function",
            "function": {
                "name": func.__name__,
                "description": (func.__doc__ or "").strip(),
                "parameters": {
                    "type": "object",
                    "properties": parameters,
                    "required": required,
                },
            },
        }


    def execute_tool_call(self, tool_call, tool_mapping, agent_name):
        """Execute a function call using the specified tool

        Args:
            tool_call (object): Object representing the function call
            tool_mapping (dict): Dict mapping function names to functions
            agent_name (str): The name of the agent executing the tool call

        Returns:
            The result of the executed function call
        """
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        print(f"{agent_name}:", f"{name}({args})")
        
        return tool_mapping[name](**args)