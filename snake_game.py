import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Set display dimensions
WIDTH = 1000
HEIGHT = 700
DISP = pygame.display.set_mode((WIDTH, HEIGHT))

# Game title
pygame.display.set_caption('Snake Game')

# Frame rate
FPS = 10
clock = pygame.time.Clock()

# Snake parameters
SNAKE_SIZE = 10
SNAKE_SPEED = 15

# Font style
font_style = pygame.font.SysFont("bahnschrift", 25)

# Function to display the score
def display_score(score):
    value = font_style.render(f"Your Score: {score}", True, WHITE)
    DISP.blit(value, [0, 0])

# Function to draw the snake
def draw_snake(snake_size, snake_list):
    for segment in snake_list:
        pygame.draw.rect(DISP, GREEN, [segment[0], segment[1], snake_size, snake_size])

# Function to display a message in the center of the screen
def display_message(msg, color):
    message = font_style.render(msg, True, color)
    DISP.blit(message, [WIDTH / 6, HEIGHT / 3])

# Main game loop
def game_loop():
    game_over = False
    game_close = False

    # Initial position of the snake
    x = WIDTH / 2
    y = HEIGHT / 2

    # Directional changes
    x_change = 0
    y_change = 0

    # Snake body and length
    snake_list = []
    snake_length = 1

    # Random position for food
    food_x = round(random.randrange(0, WIDTH - SNAKE_SIZE) / 10.0) * 10.0
    food_y = round(random.randrange(0, HEIGHT - SNAKE_SIZE) / 10.0) * 10.0

    while not game_over:

        while game_close:
            DISP.fill(BLACK)
            display_message("You Lost! Press C to Play Again or Q to Quit", RED)
            pygame.display.update()

            # Event handling for game over screen
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        # Event handling for movement
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -SNAKE_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = SNAKE_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -SNAKE_SIZE
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = SNAKE_SIZE
                    x_change = 0

        # Checking boundaries
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True

        x += x_change
        y += y_change
        DISP.fill(BLUE)

        # Drawing food
        pygame.draw.rect(DISP, RED, [food_x, food_y, SNAKE_SIZE, SNAKE_SIZE])

        # Snake movement
        snake_head = []
        snake_head.append(x)
        snake_head.append(y)
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check if snake collides with itself
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        # Draw snake and update score
        draw_snake(SNAKE_SIZE, snake_list)
        display_score(snake_length - 1)

        # Refresh the game display
        pygame.display.update()

        # Check if snake eats the food
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, WIDTH - SNAKE_SIZE) / 10.0) * 10.0
            food_y = round(random.randrange(0, HEIGHT - SNAKE_SIZE) / 10.0) * 10.0
            snake_length += 1

        clock.tick(FPS)

    pygame.quit()
    quit()

# Start the game
game_loop()
