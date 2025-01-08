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
            model_name="gemini-1.5-pro",
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
            model_name="gemini-1.5-pro",
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
async def drone_communication(drone, drone_id, message_queue):
    while True:
        # Wait for a message from the queue
        message = await message_queue.get() #waiting for msg
        print(f"[{drone_id}] Received: {message}") 

        if message["type"] == "query": # marking it as "query" so it can generate a response back
            # Process the user input and generate a response
            user_input = message["payload"]["user_input"] # payload-> contains the actual data that the system needs to process
            response_text = drone.send_message(user_input)
            print(f"[{drone_id}] Response: {response_text}")

            # Add the response back to the queue for further handling
            response_message = {
                "sender_id": drone_id,
                "type": "response",
                "payload": {
                    "status": "response processed",
                    "response": response_text,
                },
            }
            await message_queue.put(response_message)

        elif message["type"] == "end":
            print(f"[{drone_id}] Ending communication.")
            break


# Main Function
async def main():
    # Initialize drones
    drone1 = Drone1()
    drone2 = Drone2()

    # Create message queues for each drone
    message_queue1 = asyncio.Queue()
    message_queue2 = asyncio.Queue()

    # Add initial messages to the queues
    await message_queue1.put({
        "type": "query",
        "payload": {"user_input": "Locate fire in sector A. Report status."},
    })
    await message_queue2.put({
        "type": "query",
        "payload": {"user_input": "Analyze wind data and suggest adjustments."},
    })

    # Start drone communication tasks
    await asyncio.gather(
        drone_communication(drone1, "Drone1", message_queue1),
        drone_communication(drone2, "Drone2", message_queue2),
    )
   


# Run the chatbot
if __name__ == "__main__":
    asyncio.run(main())

