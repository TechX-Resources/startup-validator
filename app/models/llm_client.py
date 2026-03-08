"""
LLM client abstraction — single interface for OpenAI/Claude.
Week 2: Implement chat completion and (optional) structured output.
"""
import os
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class LLMClient:
    """Abstracted client for LLM API calls using Azure OpenAI."""

    def __init__(self):
        # Load configuration from environment variables
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4")

        if not all([api_key, azure_endpoint]):
            raise ValueError(
                "Missing required Azure OpenAI environment variables: "
                "AZURE_OPENAI_API_KEY and/or AZURE_OPENAI_ENDPOINT"
            )

        # Initialize the Azure specific client
        self.client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=azure_endpoint
        )

    def chat(self, messages: list[dict], **kwargs) -> str:
        """
        Send messages to Azure LLM and return assistant reply as string.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"Error calling Azure OpenAI API: {str(e)}")

    def chat_with_tools(self, messages: list[dict], tools: list[dict], **kwargs) -> dict:
        """
        Support tool/function calling from the API for the Validator Agent.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                tools=tools,
                **kwargs
            )
            message = response.choices[0].message
            
            result = {
                "content": message.content
            }
            
            # If the model decides to call a tool, append it to the result
            if message.tool_calls:
                result["tool_calls"] = message.tool_calls
                
            return result
        except Exception as e:
            raise RuntimeError(f"Error calling Azure OpenAI API with tools: {str(e)}")
