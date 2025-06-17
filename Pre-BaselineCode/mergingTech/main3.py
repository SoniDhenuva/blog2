import os
import google.generativeai as genai
import asyncio

updateAlertAllDrone = []

class AI:
    def __init__(self, api_key, model_name, generation_config, system_instruction):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config,
            system_instruction=system_instruction,
        )
        self.history = []

    def start_chat(self):
        return self.model.start_chat(history=self.history)

    def send_message(self, user_input):
        try:
            chat_session = self.start_chat()
            response = chat_session.send_message(user_input)
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
            system_instruction="You are an assistant that helps coordinate tasks",
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
            system_instruction="You are an assistant that helps coordinate tasks",
        )

async def drone_communication(drone, drone_id, message_queue):
    while True:
        message = await message_queue.get()
        print(f"[{drone_id}] Received: {message}")

        if message["type"] == "query":
            user_input = message["payload"]["user_input"]
            response_text = drone.send_message(user_input)
            print(f"[{drone_id}] Response: {response_text}")

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

async def chat_with_drones():
    drone1 = Drone1()
    drone2 = Drone2()
    message_queue1 = asyncio.Queue()
    message_queue2 = asyncio.Queue()

    initial_tasks = [
        drone_communication(drone1, "Drone1", message_queue1),
        drone_communication(drone2, "Drone2", message_queue2)
    ]

    user_input_tasks = asyncio.create_task(handle_user_input(message_queue1, message_queue2))
    await asyncio.gather(*initial_tasks, user_input_tasks)

async def handle_user_input(message_queue1, message_queue2):
    print("Assign Drone: Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input == "Drone1":
            user_request = input("What's the situation for Drone 1: ")
            await message_queue1.put({"type": "query", "payload": {"user_input": user_request}})
        elif user_input == "Drone2":
            user_request = input("What's the situation for Drone 2: ")
            await message_queue2.put({"type": "query", "payload": {"user_input": user_request}})
        elif user_input == "Main DB":
            user_update = input("Enter Update:")
            updateAlertAllDrone.append(user_update)
        elif user_input == "Show Main DB":
            print(updateAlertAllDrone)
        elif user_input.lower() == "exit":
            await message_queue1.put({"type": "end"})
            await message_queue2.put({"type": "end"})
            break

if __name__ == "__main__":
    asyncio.run(chat_with_drones())
