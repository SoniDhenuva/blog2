import asyncio

async def producer(queue):
    print("Producer: Adding a message")
    await queue.put("Hello, this is a test message!")

async def consumer(queue):
    print("Consumer: Waiting for a message")
    message = await queue.get()  # Retrieves a message from the queue
    print(f"Consumer: Received message: {message}")

async def main():
    queue = asyncio.Queue()  # Create the queue
    await asyncio.gather(producer(queue), consumer(queue))  # Run producer and consumer concurrently

# Run the test
if __name__ == "__main__":
    asyncio.run(main())
