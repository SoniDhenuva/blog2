import pygame
import random
import math

# Initialize pygame
pygame.init()

# Set up the screen
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Swarm Simulation")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Swarm parameters
num_agents = 100
max_speed = 4
max_force = 0.1
neighbor_radius = 50
agents = []

# Define Agent class
class Agent:
    def __init__(self, x, y):
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.acceleration = pygame.math.Vector2(0, 0)
        self.size = 5

    def update(self):
        self.velocity += self.acceleration
        # Limit speed
        if self.velocity.length() > max_speed:
            self.velocity.scale_to_length(max_speed)
        self.position += self.velocity
        # Reset acceleration
        self.acceleration *= 0

    def apply_force(self, force):
        self.acceleration += force

    def edges(self):
        if self.position.x > width:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = width
        if self.position.y > height:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = height

    def show(self):
        pygame.draw.circle(screen, WHITE, (int(self.position.x), int(self.position.y)), self.size)

    def steer_towards(self, target):
        desired = target - self.position
        desired_length = desired.length()
        if desired_length > 0:
            desired.scale_to_length(max_speed)
            steering = desired - self.velocity
            if steering.length() > max_force:
                steering.scale_to_length(max_force)
            return steering
        return pygame.math.Vector2(0, 0)

    def align(self, agents): # Each agent tries to align its velocity with nearby agents. The idea is that agents move in the same direction as their neighbors, creating a coordinated movement.
        steering = pygame.math.Vector2(0, 0)
        total = 0
        for other in agents:
            if other != self and self.position.distance_to(other.position) < neighbor_radius:
                steering += other.velocity
                total += 1
        if total > 0:
            steering /= total
            steering.scale_to_length(max_speed)
            steering -= self.velocity
            if steering.length() > max_force:
                steering.scale_to_length(max_force)
        return steering

    def cohesion(self, agents): #Each agent tries to move toward the center of mass of the nearby agents. This pulls the agents together, making the swarm act as a cohesive group.
        steering = pygame.math.Vector2(0, 0)
        total = 0
        for other in agents:
            if other != self and self.position.distance_to(other.position) < neighbor_radius:
                steering += other.position
                total += 1
        if total > 0:
            steering /= total
            steering -= self.position
            steering.scale_to_length(max_speed)
            steering -= self.velocity
            if steering.length() > max_force:
                steering.scale_to_length(max_force)
        return steering

    def separation(self, agents): #Each agent tries to avoid getting too close to other agents, preventing overcrowding. This is achieved by steering away from other agents that are too close.
        steering = pygame.math.Vector2(0, 0)
        total = 0
        for other in agents:
            distance = self.position.distance_to(other.position)
            if other != self and distance < neighbor_radius:
                diff = self.position - other.position
                diff /= distance  # Weight by distance
                steering += diff
                total += 1
        if total > 0:
            steering /= total
        if steering.length() > max_force:
            steering.scale_to_length(max_force)
        return steering

    def behavior(self, agents):
        alignment = self.align(agents)
        cohesion = self.cohesion(agents)
        separation = self.separation(agents)

        self.apply_force(alignment)
        self.apply_force(cohesion)
        self.apply_force(separation)

# Create agents
for _ in range(num_agents):
    agents.append(Agent(random.randint(0, width), random.randint(0, height)))

# Main game loop
running = True
while running:
    screen.fill(BLACK)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update and show agents
    for agent in agents:
        agent.behavior(agents)
        agent.update()
        agent.edges()
        agent.show()

    pygame.display.flip()
    pygame.time.Clock().tick(60)

# Quit pygame
pygame.quit()
