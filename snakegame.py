import pygame
import random
import sys
import json

pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
PURPLE = (150, 0, 150)
BLUE = (0, 150, 255)
BLOCK_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Snake Game")

font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

background_image = pygame.image.load("wallpaperflare.com_wallpaper (6).JPG")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

def load_best_scores():
    try:
        with open("best_scores.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_best_scores(scores):
    with open("best_scores.json", "w") as f:
        json.dump(scores, f)

def show_leaderboard(scores, recent_score):
    leaderboard_screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Leaderboard")
    running = True
    while running:
        leaderboard_screen.fill(BLACK)
        title_text = font.render("Leaderboard", True, WHITE)
        leaderboard_screen.blit(title_text, (130, 20))
        recent_text = font.render(f"Recent Score: {recent_score}", True, WHITE)
        leaderboard_screen.blit(recent_text, (100, 60))
        for i, score in enumerate(scores):
            score_text = font.render(f"{i + 1}. {score}", True, WHITE)
            leaderboard_screen.blit(score_text, (150, 100 + i * 30))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.display.set_mode((WIDTH, HEIGHT))

def show_tutorial():
    tutorial_screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("How to Play")
    running = True
    while running:
        tutorial_screen.fill(BLACK)
        lines = [
            "HOW TO PLAY",
            "Arrow Keys - Move the snake",
            "R - Restart game",
            "P - Pause/Resume",
            "S - Change snake skin",
            "Collect apples to grow",
            "Avoid barriers and yourself",
            "Press ESC to return"
        ]
        for i, line in enumerate(lines):
            text = font.render(line, True, WHITE)
            tutorial_screen.blit(text, (50, 50 + i * 40))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
    pygame.display.set_mode((WIDTH, HEIGHT))

class SnakeGame:
    def __init__(self):
        self.snake = [(200, 200), (220, 200), (240, 200)]
        self.direction = "RIGHT"
        self.new_direction = self.direction
        self.score = 0
        self.best_scores = load_best_scores()
        self.game_over = False
        self.paused = False
        self.speed = 10  
        self.shield_active = False
        self.shield_timer = 0  
        self.apple_eaten = 0  
        self.barriers = self.generate_barriers()
        self.apple = self.generate_apple()
        self.poison_apple = None
        self.shield = None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != "DOWN":
                    self.new_direction = "UP"
                elif event.key == pygame.K_DOWN and self.direction != "UP":
                    self.new_direction = "DOWN"
                elif event.key == pygame.K_LEFT and self.direction != "RIGHT":
                    self.new_direction = "LEFT"
                elif event.key == pygame.K_RIGHT and self.direction != "LEFT":
                    self.new_direction = "RIGHT"
                elif event.key == pygame.K_p:
                    self.paused = not self.paused  
                elif event.key == pygame.K_r:
                    self.__init__()

    def generate_apple(self):
        while True:
            apple = (random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
                     random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE)
            if apple not in self.snake and apple not in self.barriers:
                return apple
            
    def update(self):
        if self.game_over or self.paused:
            return

        if self.shield_active and self.shield_timer > 0:
            self.shield_timer -= 1
        elif self.shield_timer == 0:
            self.shield_active = False

        self.direction = self.new_direction
        head = self.snake[-1]
        new_head = {
            "UP": (head[0], head[1] - BLOCK_SIZE),
            "DOWN": (head[0], head[1] + BLOCK_SIZE),
            "LEFT": (head[0] - BLOCK_SIZE, head[1]),
            "RIGHT": (head[0] + BLOCK_SIZE, head[1]),
        }[self.direction]

        new_head = (new_head[0] % WIDTH, new_head[1] % HEIGHT)

        if new_head in self.snake or (new_head in self.barriers and not self.shield_active):
            self.game_over = True
            return

        self.snake.append(new_head)

        if new_head == self.apple:
            self.score += 1
            self.apple_eaten += 1  
            self.apple = self.generate_apple()  

            if self.apple_eaten % 3 == 0:  
                self.generate_powerup()

        if new_head == self.poison_apple:
            self.score -= 1  
            self.poison_apple = None  

        if new_head == self.shield:
            self.shield_active = True  
            self.shield_timer = 200  
            self.shield = None  

        if new_head != self.apple:
            self.snake.pop(0)

    def generate_powerup(self):
        powerup_type = random.choice(['poison', 'shield'])
        while True:
            powerup = (random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
                       random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE)
            if powerup not in self.snake and powerup not in self.barriers and powerup != self.apple:
                if powerup_type == 'poison':
                    self.poison_apple = powerup
                    print("Generated Poison Apple at:", self.poison_apple)
                elif powerup_type == 'shield':
                    self.shield = powerup
                    print("Generated Shield at:", self.shield)
                break 

    def generate_barriers(self):
        num_barriers = 5
        barriers = []
        for _ in range(num_barriers):
            barriers.append((random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
                             random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE))
        return barriers

    def draw(self):
        screen.blit(background_image, (0, 0))
        for barrier in self.barriers:
            pygame.draw.rect(screen, BLACK, (barrier[0], barrier[1], BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.ellipse(screen, RED, (self.apple[0], self.apple[1], BLOCK_SIZE, BLOCK_SIZE))
        if self.poison_apple:
            pygame.draw.ellipse(screen, PURPLE, (self.poison_apple[0], self.poison_apple[1], BLOCK_SIZE, BLOCK_SIZE))
        if self.shield:
            pygame.draw.circle(screen, BLUE, (self.shield[0] + BLOCK_SIZE // 2, self.shield[1] + BLOCK_SIZE // 2), BLOCK_SIZE // 2)
        for segment in self.snake:
            pygame.draw.circle(screen, GREEN, (segment[0] + BLOCK_SIZE // 2, segment[1] + BLOCK_SIZE // 2), BLOCK_SIZE // 2)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            
            if not self.paused and not self.game_over:
                self.update()

            self.draw()
            clock.tick(self.speed)

if __name__ == "__main__":
    best_scores = load_best_scores()
    recent_score = 0
    while True:
        screen.fill(BLACK)
        text = font.render("Press 'T' for Tutorial, 'L' for Leaderboard, or any key to start", True, WHITE)
        screen.blit(text, (100, HEIGHT // 2))
        pygame.display.flip()
        game = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    show_tutorial()
                elif event.key == pygame.K_l:
                    show_leaderboard(best_scores, recent_score)
                else:
                    game = SnakeGame()
                    game.run()
                    break
