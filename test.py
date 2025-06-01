import pygame

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DNA Sequencing Lab")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)

# Font
font = pygame.font.Font(None, 36)

# Game loop
running = True
while running:
    screen.fill(WHITE)

    # Display title
    text = font.render("Welcome to the DNA Sequencing Lab!", True, BLUE)
    screen.blit(text, (200, 50))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
