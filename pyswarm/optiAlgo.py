from pyswarm import pso
import google.generativeai as genai
import time
from datetime import datetime

allUpdates = {}

# Configure Gemini API
genai.configure(api_key="AIzaSyATDwSoaJAyojmZ6sloGeW0rTE5JvBY498")  # Replace with your actual API key

# Example function to analyze user input using Gemini AI
def analyze_input(user_input):
    prompt = f"""
    Given this situation update: '{user_input}', determine how to adjust task priorities.
    Respond in this format: {{'evacuation': X, 'water gathering': Y, 'fire suppression': Z}}.
    X, Y, and Z should be integers representing priority adjustments it could be -500 to 500 change depending on the serverity. but the net values that you generate must be 0
    """

    model = genai.GenerativeModel("gemini-pro") #gemini-pro
    response = model.generate_content(prompt)
    print("\n🔍 AI Response (Raw):", response.text)  # Debugging output

    
    try:
        # Convert AI response to a dictionary
        priority_changes = eval(response.text)
    except:
        priority_changes = {"evacuation": 0, "water gathering": 0, "fire suppression": 0}  # Default if AI fails

    print("📊 AI Interpreted Changes:", priority_changes)  # Debugging output
    return priority_changes

# Default priorities
desired_priorities = {
    "evacuation": 9000,
    "water gathering": 5000,
    "fire suppression": 7000
}

# Function to update priorities based on AI response
def update_priorities(user_input):
    global desired_priorities
    print("\n📝 User Input:", user_input)

    # Get AI's suggested changes
    priority_changes = analyze_input(user_input)

    # Apply AI adjustments (ensure negatives reduce values)
    for task in desired_priorities:
        new_value = desired_priorities[task] + priority_changes.get(task, 0)
        desired_priorities[task] = max(0, new_value)  # Ensure no negative priorities

    print("✅ Updated Priorities:", desired_priorities)
    return list(desired_priorities.values())  # Convert dictionary to list for PSO


# Function to get current desired priorities
def get_desired_priorities():
    return list(desired_priorities.values())

# Define the objective function for PSO
def objective(x):
    desired = get_desired_priorities()
    weights = [1, 1, 1]
    cost = sum(weights[i] * (x[i] - desired[i]) ** 2 for i in range(3))
    return cost

# Lower and upper bounds for each task's priority
lb = [0, 0, 0]  # Min priority
ub = [10000, 10000, 10000]  # Max priority

# Function to assign tasks to drones
def optimalPriorities(optimal_priorities):
    tasks = ["Evacuation", "Water Gathering", "Fire Suppression"]
    for task, priority in zip(tasks, optimal_priorities):
        print(f"Assigning task '{task}' with priority {priority:.2f}")


def assignTasksDrones(optimal_priorities):
    prompt = f"""
    Given this list of priority numbers (highest # = more priority) (numbers in order of Evacuation drone, water gathering drone,and 
    fire suppression drone)'{optimal_priorities}', adjust the number of drones on each task. Initally each (evac, water, and fire) drones have 20 in each sections.
    Respond in this format: {{'evacuationDrone#': X, 'waterGatheringDrone': Y, 'fireSuppressionDrone': Z}}. then then list how many of the drone you changed from the section. 
    For example, 5 firedrones change to evacuation drones. total number of drones must be 60.
    
    """

    model = genai.GenerativeModel("gemini-pro") #gemini-pro
    response = model.generate_content(prompt)
    status = "Done"
    print("\n🔍 AI Response FOR DRONE (Raw):", response.text)  # Debugging output

    return status

def timeStamp():
    now = datetime.now()
    timestamp_str = now.strftime("%Y%m%d%H%M%S")

    year = timestamp_str[:4]    # First 4 characters (YYYY)
    month = timestamp_str[4:6]  # Next 2 characters (MM)
    day = timestamp_str[6:8]    # Next 2 characters (DD)
    hour = timestamp_str[8:10]  # Next 2 characters (HH)
    minute = timestamp_str[10:12] # Next 2 characters (MM)
    second = timestamp_str[12:14] # Last 2 characters (SS)

    return f"Year: {year}, Month: {month}, Day: {day}, Hour: {hour}, Minute: {minute}, Second: {second}"


# Main loop
def main():
    while True:
        userInput = input("You: ")
        if userInput == "Main DB":
            user_input = input("Enter update (or 'exit' to quit): ")
            if user_input.lower() == 'exit':
                break

            allUpdates[user_input] = timeStamp() # appending into dictionary

            # Update priorities using AI analysis
            update_priorities(user_input)

            # run PSO with updated priorities
            optimal_priorities, optimal_cost = pso(objective, lb, ub, swarmsize=100, maxiter=300, omega=0.6, phip=2.0, phig=2.5)
        
            print("\nUpdated Optimal Task Priorities:", optimal_priorities)
            print("Updated Cost:", optimal_cost)
            optimalPriorities(optimal_priorities)
            tasksAssigned = assignTasksDrones(optimal_priorities)
            print(tasksAssigned)

            time.sleep(1)  # Simulate continuous operation
        if userInput == "list":
                print(allUpdates)
        

if __name__ == '__main__':
    main()
