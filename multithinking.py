# Drone 1: Positioned near a river, capable of detecting water sources.
# Drone 2: Detects people and relays information about their positions.
# Drone 3: Detects the fire's spread in the west region.

import asyncio
import random
from multiprocessing import Manager, Process

def drone_1(context, communication):
    # Drone 1: near a river
    context['drone_1'] = 'near_river'
    communication['drone_1'] = "I am near a river."

def drone_2(context, communication):
    # Drone 2: spots people nearby
    context['drone_2'] = 'sees_people'
    communication['drone_2'] = "People spotted nearby."

def drone_3(context, communication):
    # Drone 3: sees fire approaching the west
    context['drone_3'] = 'fire_west'
    communication['drone_3'] = "Fire is approaching from the west."

def decision_maker(context, communication):
    # Basic decision-making: Combining the context
    print("Communication:", communication)
    if 'near_river' in context.values() and 'sees_people' in context.values() and 'fire_west' in context.values():
        plan = "Move people away, redirect water from river, and focus on fire suppression from the west."
    else:
        plan = "Wait for more data."

    print("Operational Plan:", plan)

async def main():
    with Manager() as manager:
        context = manager.dict()  # Shared context between drones
        communication = manager.dict()  # Shared communication

        # Simulate drones' actions
        p1 = Process(target=drone_1, args=(context, communication))
        p2 = Process(target=drone_2, args=(context, communication))
        p3 = Process(target=drone_3, args=(context, communication))
        
        p1.start()
        p2.start()
        p3.start()

        p1.join()
        p2.join()
        p3.join()

        # Decision-making based on communication
        decision_maker(context, communication)

# Run the simulation
if __name__ == "__main__":
    asyncio.run(main())
