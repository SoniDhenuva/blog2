import asyncio

situation = input("What is the situation: ")

# AI Module 1 - Sends data
async def ai_module_1():
    await asyncio.sleep(1)  # Simulate processing time
    print("AI Module 1 processed data")
    return situation

# AI Module 2 - Receives and processes data
async def ai_module_2():
    result = await ai_module_1()  # Await data from Module 1
    print(f"AI Module 2 received: {result}")
    return "Processed by AI Module 2"

# Main function to run the asyncio tasks
async def main():
    result = await ai_module_2()  # Start the communication process
    print(f"Final result: {result}")

# Run the asynchronous tasks
asyncio.run(main())
