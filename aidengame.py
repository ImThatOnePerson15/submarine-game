import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1500, 1200
PAUSE_COUNT = 1000

# Colors
WHITE = (255, 255, 255)
SKYBLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Underwater Submarine Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()
random_number = random.randint(0, 9)

# Load submarine
submarine = pygame.image.load('suber.png')  # Replace with a valid path or use a placeholder
submarine = pygame.transform.scale(submarine, (100, 50))
submarine_rect = submarine.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Fish settings
fish_img = pygame.image.load('carp.png')  # Replace with a valid path or use a placeholder
fish_img = pygame.transform.scale(fish_img, (50, 30))

trash_img = pygame.image.load('trash.png')  # Replace with a valid path or use a placeholder
trash_img = pygame.transform.scale(trash_img, (50, 30))

# Initialize game variables
trash_list = []
for _ in range(15):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    speedfortrash = random.randint(2, 5)
    trash_list.append({"rect": pygame.Rect(x, y, 50, 30), "speedfortrash": speedfortrash})

fish_list = []
for _ in range(30):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    speed = random.randint(2, 5)
    fish_list.append({"rect": pygame.Rect(x, y, 50, 30), "speed": speed})

score = 0
health = 100
paused = False  # Added pause variable

# Font
font = pygame.font.Font(None, 36)

# Game loop
running = True
while running:
    screen.fill(SKYBLUE)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused  # Toggle pause

    if not paused:
        # Controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and submarine_rect.top > 0:
            submarine_rect.y -= 5
        if keys[pygame.K_DOWN] and submarine_rect.bottom < HEIGHT:
            submarine_rect.y += 5
        if keys[pygame.K_LEFT] and submarine_rect.left > 0:
            submarine_rect.x -= 5
        if keys[pygame.K_RIGHT] and submarine_rect.right < WIDTH:
            submarine_rect.x += 5

        # Move fish
        for fish in fish_list:
            fish["rect"].x -= fish["speed"]
            if fish["rect"].right < 0:
                fish["rect"].x = WIDTH
                fish["rect"].y = random.randint(0, HEIGHT)
                fish["speed"] = random.randint(2, 5)

        for trash in trash_list:
            trash["rect"].x -= trash["speedfortrash"]
            if trash["rect"].right < 0:
                trash["rect"].x = WIDTH
                trash["rect"].y = random.randint(0, HEIGHT)
                trash["speedfortrash"] = random.randint(2, 5)

        # Check collisions
        for fish in fish_list:
            if submarine_rect.colliderect(fish["rect"]):
                health -= 10
                fish["rect"].x = WIDTH
                fish["rect"].y = random.randint(0, HEIGHT)
                fish["speed"] = random.randint(2, 5)

        for trash in trash_list:
            if submarine_rect.colliderect(trash["rect"]):
                score += 500
                trash["rect"].x = WIDTH
                trash["rect"].y = random.randint(0, HEIGHT)
                trash["speedfortrash"] = random.randint(2, 5)

        # Update score
        score += 1
        if score % PAUSE_COUNT == 0:
            paused = True
            random_number = random.randint(0, 9)

    # Draw submarine
    screen.blit(submarine, submarine_rect)

    # Draw fish and trash
    for fish in fish_list:
        screen.blit(fish_img, fish["rect"])
    for trash in trash_list:
        screen.blit(trash_img, trash["rect"])

    # Draw health bar
    pygame.draw.rect(screen, RED, (10, 10, 200, 20))
    pygame.draw.rect(screen, GREEN, (10, 10, max(0, 200 * (health / 100)), 20))

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 40))

    # Pause message
    if paused:
        pause_text = font.render(f"Do you know: blah blah blah: random number {random_number}", True, WHITE)
        screen.blit(pause_text, (WIDTH // 2 - 20, HEIGHT // 2 - 0))

    # Game over
    if health <= 0:
        game_over_text = font.render("Game Over!", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 20))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    # Update display
    pygame.display.flip()
    clock.tick(50)

# Quit pygame
pygame.quit()


