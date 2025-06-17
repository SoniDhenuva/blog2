import os
import google.generativeai as genai
import asyncio
import time

# List to store alerts for all drones
updateAlertAllDrone = []

class AI:
    def __init__(self, api_key, model_name, generation_config, system_instruction):
        """
        Initializes the AI model with the given configuration.
        
        Parameters:
        - api_key (str): API key for authentication.
        - model_name (str): Name of the generative AI model.
        - generation_config (dict): Configuration settings for the model.
        - system_instruction (str): Instruction to guide the model's behavior.
        """
        genai.configure(api_key=api_key)  # Configure the API key
        
        # Initialize the AI model with provided settings
        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config,
            system_instruction=system_instruction,
        )
        self.history = []  # Stores chat history for context retention
    
    def start_chat(self):
        """Starts a chat session with the configured model."""
        return self.model.start_chat(history=self.history)
    
    def send_message(self, user_input):
        """
        Processes user input and gets a response from the AI model.
        
        Parameters:
        - user_input (str): The message sent to the AI.
        
        Returns:
        - str: The response from the AI model or an error message.
        """
        try:
            # Start a chat session
            chat_session = self.start_chat()
            
            # Get the response from the AI model
            response = chat_session.send_message(user_input)
            
            # Update conversation history
            self.history.append({"role": "user", "parts": [user_input]})
            self.history.append({"role": "assistant", "parts": [response.text]})
            
            return response.text  # Return AI response
        except Exception as e:
            return f"An error occurred: {e}"  # Handle and return error message


class Drone1(AI):
    def __init__(self):
        """
        Initializes Drone1 with specific AI model configurations.
        """
        super().__init__(
            api_key="AIzaSyATDwSoaJAyojmZ6sloGeW0rTE5JvBY498",  # API Key
            model_name="gemini-1.5-pro",  # Model Name
            generation_config={
                "temperature": 1.15,  # Controls randomness of responses
                "top_p": 0.95,  # Controls diversity of responses
                "top_k": 40,  # Number of highest probability tokens considered
                "max_output_tokens": 8192,  # Maximum number of output tokens
                "response_mime_type": "text/plain",  # Response format
            },
            system_instruction=(
                "You are an assistant that helps coordinate tasks"  # AI's role
            ),
        )


class Drone2(AI):
    def __init__(self):
        """
        Initializes Drone2 with specific AI model configurations.
        """
        super().__init__(
            api_key="AIzaSyATDwSoaJAyojmZ6sloGeW0rTE5JvBY498",  # API Key
            model_name="gemini-1.5-pro",  # Model Name
            generation_config={
                "temperature": 1.15,  # Controls randomness of responses
                "top_p": 0.95,  # Controls diversity of responses
                "top_k": 40,  # Number of highest probability tokens considered
                "max_output_tokens": 8192,  # Maximum number of output tokens
                "response_mime_type": "text/plain",  # Response format
            },
            system_instruction=(
                "You are an assistant that helps coordinate tasks"  # AI's role
            ),
        )

if __name__ == "__main__":
    # Create instances of Drone1 and Drone2
    drone1 = Drone1()
    drone2 = Drone2()

    # Test sending messages
    test_message = input("You: ")

    print("Testing Drone1:")
    response1 = drone1.send_message(test_message)
    print("Drone1 Response:", response1)

