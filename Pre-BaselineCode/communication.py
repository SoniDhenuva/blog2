import asyncio
import google.generativeai as genai

# Set your Gemini API key
genai.configure(api_key="API_KEY")

# Simulated drone context
drone_contexts = {
    "drone_1": {"location": "near_river", "status": "idle"},
    "drone_2": {"location": "near_people", "status": "idle"},
    "drone_3": {"location": "near_fire", "status": "idle"},
}

# Function to communicate using AI (simulating swarm AI)
async def get_ai_response(drones, new_input):
    prompt = """
    The drones are collaborating to respond to an emergency situation. The inputs are:
    """
    for drone, context in drones.items():
        prompt += f"{drone}: Location: {context['location']}, Status: {context['status']}\n"

    prompt += f"\nNew input: {new_input}. What should the drones do next?\n"

    # Make an API call to Gemini for decision-making
    response = genai.generate_text(
        model="gemini-1",
        prompt=prompt,
        max_output_tokens=200
    )

    return response.result.strip()

# Function to simulate drone operations
async def simulate_drone_operations():
    while True:
        # User input (this could be real-time data in a more complex system)
        new_input = input("\nEnter new environmental input (e.g., 'fire approaching', 'people nearby', 'river flooding'): ")

        if new_input.lower() == 'exit':
            print("Exiting simulation.")
            break

        # Simulate drone context updates based on input (this would happen dynamically in a real system)
        if 'fire' in new_input:
            drone_contexts['drone_1']['status'] = 'assisting with water supply'
            drone_contexts['drone_2']['status'] = 'evacuating people'
            drone_contexts['drone_3']['status'] = 'monitoring fire spread'
        elif 'people' in new_input:
            drone_contexts['drone_1']['status'] = 'searching for water sources'
            drone_contexts['drone_2']['status'] = 'guiding people to safety'
            drone_contexts['drone_3']['status'] = 'monitoring fire direction'
        elif 'river' in new_input:
            drone_contexts['drone_1']['status'] = 'flood monitoring'
            drone_contexts['drone_2']['status'] = 'assisting with evacuation'
            drone_contexts['drone_3']['status'] = 'notifying fire direction'

        # Get the AI response based on the updated context and input
        response = await asyncio.to_thread(get_ai_response, drone_contexts, new_input)

        print("\nAI Generated Operational Plan:")
        print(response)

# Main function to run the simulation
async def main():
    print("Drone AI Collaboration Simulation Started.")
    await simulate_drone_operations()

if __name__ == "__main__":
    asyncio.run(main())
