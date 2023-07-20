import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 2000, 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jumping Ball")

# Load and scale the background image
background_image = pygame.image.load("Images\Background.jpg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Ball properties
circle_radius = 100
circle_x = screen_width // 2
circle_y = screen_height - circle_radius
jump_velocity = 0.5  # Initial jump velocity
gravity = 0.1  # Gravity applied each frame
jump_strength = 5  # Additional jump strength when 'J' key is pressed

# Load and scale the ball image
ball_image = pygame.image.load("Images\Boy.png")
ball_image = pygame.transform.scale(ball_image, (circle_radius * 2, circle_radius * 2))

# Square obstacle properties
obstacle_width = 200
obstacle_height = 200
obstacle_x = screen_width
obstacle_y = screen_height - obstacle_height

# Load and scale the obstacle image
obstacle_image = pygame.image.load("Images\Ball.png")
obstacle_image = pygame.transform.scale(obstacle_image, (obstacle_width, obstacle_height))

# Load and scale the game over image
game_over_image = pygame.image.load("Images\Game over.png")
game_over_image = pygame.transform.scale(game_over_image, (500, 200))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()

# Variables for high score and obstacle crossing
obstacles_crossed = 0
obstacle_crossed = False

# Variable to track initial floating time
initial_float_time = 2000  # 1 second

def draw_circle():
    screen.blit(ball_image, (circle_x - circle_radius, circle_y - circle_radius))

def draw_obstacle():
    screen.blit(obstacle_image, (obstacle_x, obstacle_y))

def check_collision():
    global obstacles_crossed, obstacle_crossed
    circle_rect = pygame.Rect(circle_x - circle_radius, circle_y - circle_radius, circle_radius * 2, circle_radius * 2)
    obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)
    if circle_rect.colliderect(obstacle_rect):
        game_over_screen()
        return True
    elif obstacle_x + obstacle_width < circle_x - circle_radius and not obstacle_crossed:
        obstacles_crossed += 1
        obstacle_crossed = True
    elif circle_y - circle_radius <= 0 or circle_y + circle_radius >= screen_height:
        game_over_screen()
        return True
    return False

def restart_game():
    global circle_x, circle_y, jump_velocity, obstacle_x, obstacle_y, obstacles_crossed, obstacle_crossed
    circle_x = screen_width // 2
    circle_y = screen_height // 2
    jump_velocity = 0
    obstacle_x = screen_width
    obstacle_y = screen_height - obstacle_height
    obstacles_crossed = 0
    obstacle_crossed = False



def game_over_screen():
    global game_over_y
    game_over_y = screen_height // 2 - 100  # Set the initial y-coordinate of the game over image

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    restart_game()
                    return

        # Move the game over image up on each frame until it reaches the top of the screen (leaving 5 lines on top)
        if game_over_y > 100:
            game_over_y -= 2

        screen.blit(background_image, (0, 0))  # Draw the background first
        screen.blit(game_over_image, (screen_width // 2 - 250, game_over_y))  # Then draw the game over image

        font = pygame.font.Font(None, 36)
        quit_text = font.render("Press Q to Quit", True, BLACK)
        restart_text = font.render("Press R to Restart", True, BLACK)
        screen.blit(quit_text, (screen_width // 2 - 80, game_over_y + 200))
        screen.blit(restart_text, (screen_width // 2 - 100, game_over_y + 250))
        score_text = font.render("High Score: " + str(obstacles_crossed), True, BLACK)
        screen.blit(score_text, (screen_width // 2 - 80, game_over_y + 150))
        pygame.display.flip()

        # Limit the frame rate to 60 FPS
        clock.tick(60)



def start_screen():
    font = pygame.font.Font(None, 36)
    start_text = font.render("Press SPACE to Jump", True, WHITE)
    screen.blit(start_text, (screen_width // 2 - 100, screen_height // 2))
    pygame.display.flip()
    pygame.time.wait(1000)  # Wait for 1 second

    screen.blit(background_image, (0, 0))
    pygame.display.flip()

start_screen()

# Timer variables
start_time = pygame.time.get_ticks()  # Get the start time
speed_increase_interval = 10000  # Increase speed every 1 minute (60000 milliseconds)
speed_increase_amount = 3  # Amount by which to increase the speed

floating_time = 0  # Keep track of floating time

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jump_velocity -= jump_strength

    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - start_time

    if elapsed_time < initial_float_time:
        # Fish floats for 1 second
        circle_y -= 1  # Adjust the fish's y position to make it float upwards
    else:
        # Update circle position
        circle_y += jump_velocity
        jump_velocity += gravity

        # Check if the circle is below or above the screen
        if circle_y > screen_height - circle_radius:
            circle_y = screen_height - circle_radius
            jump_velocity = 0
        elif circle_y < 0 + circle_radius:
            circle_y = 0 + circle_radius

    # Update obstacle position and speed
    obstacle_x -= 2 + (pygame.time.get_ticks() - start_time) // speed_increase_interval * speed_increase_amount

    # Check collision
    if check_collision():
        continue

    # Spawn new obstacles
    if obstacle_x + obstacle_width < 0:
        obstacle_x = screen_width
        obstacle_y = random.randint(0, screen_height - obstacle_height)
        obstacle_crossed = False

    # Clear the screen and draw the background image
    screen.blit(background_image, (0, 0))

    # Draw the circle and obstacle
    draw_circle()
    draw_obstacle()

    # Display the number of obstacles crossed
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(obstacles_crossed), True, WHITE)
    screen.blit(score_text, (20, 20))

    # Update the display
    pygame.display.flip()

    # Limit the frame rate to 60 FPS
    clock.tick(60)
