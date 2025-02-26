import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 180, 0)  
BLACK = (0, 0, 0)
BLOCK_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Snake Game")

font = pygame.font.Font(None, 36)

background_image = pygame.image.load("wallpaperflare.com_wallpaper (6).JPG")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

try:
    apple_image = pygame.image.load("apple.png")
    apple_image = pygame.transform.scale(apple_image, (BLOCK_SIZE, BLOCK_SIZE))
    golden_apple_image = pygame.image.load("golden_apple.png")
    golden_apple_image = pygame.transform.scale(golden_apple_image, (BLOCK_SIZE, BLOCK_SIZE))
    poison_apple_image = pygame.image.load("poison_apple.png")
    poison_apple_image = pygame.transform.scale(poison_apple_image, (BLOCK_SIZE, BLOCK_SIZE))
    speed_boost_image = pygame.image.load("speed_boost.jpg")
    speed_boost_image = pygame.transform.scale(speed_boost_image, (BLOCK_SIZE, BLOCK_SIZE))
    shield_image = pygame.image.load("shield.jpg")
    shield_image = pygame.transform.scale(shield_image, (BLOCK_SIZE, BLOCK_SIZE))
    slowdown_image = pygame.image.load("slowdown.png")
    slowdown_image = pygame.transform.scale(slowdown_image, (BLOCK_SIZE, BLOCK_SIZE))
except:
    apple_image = None  
    golden_apple_image = None
    poison_apple_image = None
    speed_boost_image = None
    shield_image = None
    slowdown_image = None

try:
    snake_skin_images = [
        pygame.image.load("snake_skin_1.jpg"),
        pygame.image.load("snake_skin_2.jpg"),
        pygame.image.load("snake_skin_3.jpg"),
    ]
    for i in range(len(snake_skin_images)):
        snake_skin_images[i] = pygame.transform.scale(snake_skin_images[i], (BLOCK_SIZE, BLOCK_SIZE))
except:
    snake_skin_images = None

clock = pygame.time.Clock()


class SnakeGame:
    def __init__(self):
        self.snake = [(200, 200), (220, 200), (240, 200)]
        self.direction = "RIGHT"
        self.new_direction = self.direction  
        self.barriers = self.generate_barriers()  
        self.power_ups = []  # Initialize power_ups here
        self.apple = self.generate_apple()
        self.apple_type = "normal"
        self.score = 0
        self.best_score = self.load_best_score()
        self.game_over = False
        self.difficulty_level = 1
        self.snake_skin = 0
        self.combo_count = 0
        self.timer = 60  # Countdown timer for the game
        self.speed_boost_active = False
        self.shield_active = False
        self.slowdown_active = False

    def generate_apple(self):
        while True:
            x = random.randint(0, WIDTH - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE
            y = random.randint(0, HEIGHT - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE
            if (x, y) not in self.snake and (x, y) not in self.barriers and (x, y) not in self.power_ups:
                return (x, y)

    def generate_barriers(self):
        barriers = []
        for _ in range(10):
            x = random.randint(0, WIDTH - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE
            y = random.randint(0, HEIGHT - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE
            barriers.append((x, y))
        return barriers

    def generate_power_up(self):
        while True:
            x = random.randint(0, WIDTH - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE
            y = random.randint(0, HEIGHT - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE
            if (x, y) not in self.snake and (x, y) not in self.barriers and (x, y) not in self.power_ups:
                return (x, y)

    def load_best_score(self):
        try:
            with open("best_score.txt", "r") as f:
                return int(f.read())
        except FileNotFoundError:
            return 0

    def save_best_score(self):
        with open("best_score.txt", "w") as f:
            f.write(str(self.best_score))

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
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
                elif event.key == pygame.K_s:
                    self.snake_skin = (self.snake_skin + 1) % len(snake_skin_images)

    def reset_game(self):
        self.game_over = False
        self.snake = [(200, 200), (220, 200), (240, 200)]
        self.direction = "RIGHT"
        self.new_direction = self.direction
        self.apple = self.generate_apple()
        self.apple_type = "normal"
        self.score = 0
        self.difficulty_level = 1
        self.barriers = self.generate_barriers()
        self.power_ups = []
        self.combo_count = 0
        self.timer = 60
        self.speed_boost_active = False
        self.shield_active = False
        self.slowdown_active = False

    def update(self):
        if not self.game_over:
            self.direction = self.new_direction  

            head = self.snake[-1]
            if self.direction == "UP":
                new_head = (head[0], head[1] - BLOCK_SIZE)
            elif self.direction == "DOWN":
                new_head = (head[0], head[1] + BLOCK_SIZE)
            elif self.direction == "LEFT":
                new_head = (head[0] - BLOCK_SIZE, head[1])
            elif self.direction == "RIGHT":
                new_head = (head[0] + BLOCK_SIZE, head[1])

            new_head = (
                new_head[0] % WIDTH,
                new_head[1] % HEIGHT
            )

            if new_head in self.snake:
                if not self.shield_active:
                    self.game_over = True
                    return

            if new_head in self.barriers:
                if not self.shield_active:
                    self.game_over = True
                    return

            self.snake.append(new_head)

            if self.snake[-1] == self.apple:
                if self.apple_type == "normal":
                    self.score += 1
                    self.combo_count += 1
                elif self.apple_type == "golden":
                    self.score += 3
                    self.combo_count += 1
                elif self.apple_type == "poison":
                    self.snake.pop(0)
                    self.combo_count = 0
                self.apple = self.generate_apple()
                self.apple_type = random.choice(["normal", "golden", "poison"])
                self.spawn_power_up()
            else:
                self.snake.pop(0)

            if self.score > self.best_score:
                self.best_score = self.score
                self.save_best_score()

            if self.score % 10 == 0 and self.score != 0:
                self.difficulty_level += 1

            self.update_power_ups()
            self.update_timer()

    def spawn_power_up(self):
        if random.random() < 0.3:  # 30% chance to spawn a power-up
            power_up_type = random.choice(["speed", "shield", "slowdown"])
            power_up_position = self.generate_power_up()
            self.power_ups.append((power_up_position, power_up_type))

    def update_power_ups(self):
        for power_up in self.power_ups:
            if power_up[0] in self.snake:
                if power_up[1] == "speed":
                    self.speed_boost_active = True
                elif power_up[1] == "shield":
                    self.shield_active = True
                elif power_up[1] == "slowdown":
                    self.slowdown_active = True
                self.power_ups.remove(power_up)

    def update_timer(self):
        if self.timer > 0:
            self.timer -= 1 / (10 + self.difficulty_level)
        else:
            self.game_over = True

    def draw(self):
        screen.blit(background_image, (0, 0))

        if not self.game_over:
            for barrier in self.barriers:
                pygame.draw.rect(screen, BLACK, (barrier[0], barrier[1], BLOCK_SIZE, BLOCK_SIZE))

            for i, pos in enumerate(self.snake):
                glow_rect = pygame.Rect(pos[0] - 2, pos[1] - 2, BLOCK_SIZE + 4, BLOCK_SIZE + 4)
                pygame.draw.rect(screen, (0, 100, 0, 100), glow_rect, border_radius=8)

                color_variation = 50 if i % 2 == 0 else 0
                body_color = (0, 255 - color_variation, 0)

                if snake_skin_images:
                    screen.blit(snake_skin_images[self.snake_skin], (pos[0], pos[1]))
                else:
                    pygame.draw.rect(screen, body_color, (pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE), border_radius=10)

                inner_rect = pygame.Rect(pos[0] + 3, pos[1] + 3, BLOCK_SIZE - 6, BLOCK_SIZE - 6)
                pygame.draw.rect(screen, (0, 200 - color_variation, 0), inner_rect, border_radius=8)

            head_x, head_y = self.snake[-1]
            pygame.draw.circle(screen, BLACK, (head_x + 4, head_y + 4), 3)
            pygame.draw.circle(screen, BLACK, (head_x + BLOCK_SIZE - 8, head_y + 4), 3)

            if apple_image:
                if self.apple_type == "normal":
                    screen.blit(apple_image, (self.apple[0], self.apple[1]))
                elif self.apple_type == "golden":
                    screen.blit(golden_apple_image, (self.apple[0], self.apple[1]))
                elif self.apple_type == "poison":
                    screen.blit(poison_apple_image, (self.apple[0], self.apple[1]))
            else:
                if self.apple_type == "normal":
                    pygame.draw.ellipse(screen, (200, 0, 0), (self.apple[0], self.apple[1], BLOCK_SIZE, BLOCK_SIZE))
                elif self.apple_type == "golden":
                    pygame.draw.ellipse(screen, (255, 215, 0), (self.apple[0], self.apple[1], BLOCK_SIZE, BLOCK_SIZE))
                elif self.apple_type == "poison":
                    pygame.draw.ellipse(screen, (139, 0, 0), (self.apple[0], self.apple[1], BLOCK_SIZE, BLOCK_SIZE))

            for power_up in self.power_ups:
                if power_up[1] == "speed":
                    if speed_boost_image:
                        screen.blit(speed_boost_image, power_up[0])
                    else:
                        pygame.draw.rect(screen, (0, 0, 255), (power_up[0][0], power_up[0][1], BLOCK_SIZE, BLOCK_SIZE))
                elif power_up[1] == "shield":
                    if shield_image:
                        screen.blit(shield_image, power_up[0])
                    else:
                        pygame.draw.rect(screen, (255, 255, 0), (power_up[0][0], power_up[0][1], BLOCK_SIZE, BLOCK_SIZE))
                elif power_up[1] == "slowdown":
                    if slowdown_image:
                        screen.blit(slowdown_image, power_up[0])
                    else:
                        pygame.draw.rect(screen, (255, 0, 255), (power_up[0][0], power_up[0][1], BLOCK_SIZE, BLOCK_SIZE))

            score_text = font.render(f"Score: {self.score}", True, WHITE)
            screen.blit(score_text, (10, 10))
            best_score_text = font.render(f"Best Score: {self.best_score}", True, WHITE)
            screen.blit(best_score_text, (10, 40))
            difficulty_text = font.render(f"Difficulty: {self.difficulty_level}", True, WHITE)
            screen.blit(difficulty_text, (10, 70))
            timer_text = font.render(f"Time: {int(self.timer)}", True, WHITE)
            screen.blit(timer_text, (10, 100))
            combo_text = font.render(f"Combo: {self.combo_count}", True, WHITE)
            screen.blit(combo_text, (10, 130))

        else:
            game_over_text = font.render("Game Over!", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - 75, HEIGHT // 2 - 18))
            restart_text = font.render("Press 'R' to restart", True, WHITE)
            screen.blit(restart_text, (WIDTH // 2 - 100, HEIGHT // 2 + 50))

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(10 + self.difficulty_level)  


if __name__ == "__main__":
    game = SnakeGame()
    game.run()