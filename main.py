import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Game window settings
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catch the Ball")

# Constants
BALL_SIZE = 20
CONTAINER_WIDTH = 100
CONTAINER_HEIGHT = 20
CONTAINER_COLOR = RED
FPS = 60

clock = pygame.time.Clock()

class Ball:
    def __init__(self, speed):
        self.x = random.randint(0, SCREEN_WIDTH - BALL_SIZE)
        self.y = 0
        self.speed = speed
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    def fall(self):
        self.y += self.speed
    
    def draw(self):
        pygame.draw.circle(SCREEN, self.color, (self.x, self.y), BALL_SIZE)

class Container:
    def __init__(self):
        self.width = CONTAINER_WIDTH
        self.height = CONTAINER_HEIGHT
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - self.height
        self.speed = 5
    
    def move_left(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = 0
    
    def move_right(self):
        self.x += self.speed
        if self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
    
    def draw(self):
        pygame.draw.rect(SCREEN, CONTAINER_COLOR, (self.x, self.y, self.width, self.height))

def increase_ball_speed(balls):
    for ball in balls:
        ball.speed += 1

def main():
    running = True
    balls = []
    container = Container()
    score = 0
    errors = 0
    ball_speed = None  # Initialize ball speed to None
    last_speed_increase = pygame.time.get_ticks()
    difficulty_selected = False  # Variable to track if difficulty is selected

    # Font initialization
    font = pygame.font.Font(None, 36)

    while running:
        SCREEN.fill(WHITE)

        if not difficulty_selected:  # Display difficulty selection menu if difficulty is not selected
            # Draw difficulty selection menu
            difficulty_text = font.render("Select difficulty:", True, BLACK)
            SCREEN.blit(difficulty_text, (50, 50))

            easy_text = font.render("Easy", True, BLACK)
            SCREEN.blit(easy_text, (50, 100))

            medium_text = font.render("Medium", True, BLACK)
            SCREEN.blit(medium_text, (50, 150))

            osu_text = font.render("Osu Player", True, BLACK)
            SCREEN.blit(osu_text, (50, 200))

            arcade_text = font.render("Arcade Ultimax", True, BLACK)
            SCREEN.blit(arcade_text, (50, 250))

        pygame.display.flip()

        # Event handling for selecting difficulty
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not difficulty_selected:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 50 <= mouse_x <= 250:
                    if 100 <= mouse_y <= 130:
                        ball_speed = 1.5
                        difficulty_selected = True
                    elif 150 <= mouse_y <= 180:
                        ball_speed = 3
                        difficulty_selected = True
                    elif 200 <= mouse_y <= 230:
                        ball_speed = 5
                        difficulty_selected = True
                    elif 250 <= mouse_y <= 280:
                        ball_speed = 2
                        difficulty_selected = True

        if difficulty_selected:  # Start the game if difficulty is selected
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                container.move_left()
            if keys[pygame.K_RIGHT]:
                container.move_right()

            mouse_x, _ = pygame.mouse.get_pos()
            container.x = mouse_x - container.width / 2
            if container.x < 0:
                container.x = 0
            elif container.x > SCREEN_WIDTH - container.width:
                container.x = SCREEN_WIDTH - container.width

            current_time = pygame.time.get_ticks()
            if current_time - last_speed_increase > 20000:  # Increase speed every 20 seconds
                increase_ball_speed(balls)
                last_speed_increase = current_time

            if random.randint(0, 100) < 5:
                balls.append(Ball(ball_speed))

            for ball in balls:
                ball.fall()
                ball.draw()
                if ball.y > SCREEN_HEIGHT:
                    balls.remove(ball)
                    if ball_speed == 2:  # Only count errors in Arcade Ultimax mode
                        errors += 1
                        if errors >= 6:  # Game over if maximum errors reached
                            running = False

            container.draw()

            for ball in balls:
                if (ball.y + BALL_SIZE >= container.y and
                    ball.x + BALL_SIZE >= container.x and
                    ball.x <= container.x + container.width):
                    balls.remove(ball)
                    score += 10
            
            text = font.render("Score: " + str(score), True, BLACK)
            SCREEN.blit(text, (10, 10))

            if ball_speed == 2:  # Only display errors in Arcade Ultimax mode
                errors_text = font.render("Errors: " + str(errors) + "/6", True, BLACK)
                SCREEN.blit(errors_text, (10, 50))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()