import os
import google.generativeai as genai
import asyncio

updateAlertAllDrone = []

class AI:
    def __init__(self, api_key, model_name, generation_config, system_instruction):
        # Configure the API key
        genai.configure(api_key=api_key)
        
        # Initialize the model
        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config,
            system_instruction=system_instruction,
        )
        self.history = []
    
    def start_chat(self):
        """Starts a chat session with the configured model."""
        return self.model.start_chat(history=self.history)
    
    def send_message(self, user_input):
        """Processes user input and gets a response from the model."""
        try:
            # Start a chat session
            chat_session = self.start_chat()
            
            # Get the response from the model
            response = chat_session.send_message(user_input)
            
            # Update conversation history
            self.history.append({"role": "user", "parts": [user_input]})
            self.history.append({"role": "assistant", "parts": [response.text]})
            
            return response.text
        except Exception as e:
            return f"An error occurred: {e}"


class Drone1(AI):
    def __init__(self):
        super().__init__(
            api_key="AIzaSyC6NFPqfHQSACtkt3-gou52RlbbQWOibFo",
            model_name="gemini-2.0-flash-thinking-exp-1219",
            generation_config={
                "temperature": 1.15,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            },
            system_instruction=(
                "You are an assistant that helps coordinate tasks"
            ),
        )

class Drone2(AI):
    def __init__(self):
        super().__init__(
            api_key="AIzaSyC6NFPqfHQSACtkt3-gou52RlbbQWOibFo",
            model_name="gemini-2.0-flash-thinking-exp-1219",
            generation_config={
                "temperature": 1.15,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            },
            system_instruction=(
                "You are an assistant that helps coordinate tasks"
            ),
        )



# Run the chatbot
if __name__ == "__main__":
    print("Assign Drone: ")

    while True:
        user_input = input("You: ")
        if user_input == "Drone1":
            chatbot = Drone1()
            user_request = input("Whats the situation for Drone 1: ")
            response = chatbot.send_message(user_request)
            print(f'Drone1: {response}\n')
        elif user_input == "Drone2":
            chatbot = Drone2()
            user_request = input("Whats the situation for Drone 1: ")
            response = chatbot.send_message(user_request)
            print(f'Drone2: {response}\n')
        elif user_input == "Main DB":
            user_update = input("Enter Update:")
            updateAlertAllDrone.append(user_update)
        elif user_input == "Show Main DB":
            print(updateAlertAllDrone)


