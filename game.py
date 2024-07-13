import pygame
import sys
import random
from globals import *
from levels import *

class Player(pygame.sprite.Sprite):
    def __init__(self, display, color):
        super().__init__()
        self.display = display
        self.speed = SPEED
        self.acceleration = ACCELERATION
        self.damage = PLAYER_DAMAGE
        self.health = HEALTH
        self.position = vector(WIDTH // 2, HEIGHT // 2)
        self.velocity = vector(0, 0)
        self.size = (25, 25)
        self.color = color
        self.rect = pygame.Rect(*self.position, *self.size)
        self.font = pygame.font.SysFont("arial", 25, bold=True)
        self.inside_house = False
        self.current_house = None

    def draw_player(self, camera_offset):
        self.rect.topleft = self.position + camera_offset
        pygame.draw.rect(self.display, self.color, self.rect)

    def update_player(self, dt, houses):
        keys = pygame.key.get_pressed()
        self.player_move(keys, dt)
        self.rect.topleft = self.position
        self.check_collision(houses)

    def player_move(self, keys, dt):
        # Movement keys mapped for smoother key response
        movement_keys = {
            pygame.K_LEFT: (-1, 0),
            pygame.K_a: (-1, 0),
            pygame.K_RIGHT: (1, 0),
            pygame.K_d: (1, 0),
            pygame.K_UP: (0, -1),
            pygame.K_w: (0, -1),
            pygame.K_DOWN: (0, 1),
            pygame.K_s: (0, 1)
        }

        # Calculate velocity
        velocity = vector(0, 0)
        for key, (dx, dy) in movement_keys.items():
            if keys[key]:
                velocity += vector(dx, dy)

        # Set velocity
        if velocity.length() > 0:
            velocity = velocity.normalize() * self.speed
        # Slower acceleration
        self.velocity += (velocity - self.velocity) * (self.acceleration * dt)
        # Update position
        self.position += self.velocity * dt
        # Keep player within area
        self.position.x = max(0, min(self.position.x, 2500 - 25))
        self.position.y = max(0, min(self.position.y, 2500 - 25))

    def check_collision(self, houses):
        player_rect = self.rect.copy()
        for house in houses:
            if player_rect.colliderect(house.rect):
                if player_rect.colliderect(house.entrance_rect):
                    self.position = self.enter_house(house)
                else:
                    self.wall_collision(player_rect, house)

    def wall_collision(self, player_rect, house):
        for wall in house.walls:
            if player_rect.colliderect(wall):
                # Calculate the overlap in both axes
                overlap_left = player_rect.right - wall.left
                overlap_right = wall.right - player_rect.left
                overlap_top = player_rect.bottom - wall.top
                overlap_bottom = wall.bottom - player_rect.top

                # Get the smallest overlap direction
                if overlap_left < overlap_right and overlap_left < overlap_top and overlap_left < overlap_bottom:
                    self.position.x = wall.left - self.size[0]  # Push left
                    self.velocity.x = 0
                elif overlap_right < overlap_left and overlap_right < overlap_top and overlap_right < overlap_bottom:
                    self.position.x = wall.right  # Push right
                    self.velocity.x = 0
                elif overlap_top < overlap_left and overlap_top < overlap_right and overlap_top < overlap_bottom:
                    self.position.y = wall.top - self.size[1]  # Push up
                    self.velocity.y = 0
                elif overlap_bottom < overlap_left and overlap_bottom < overlap_right and overlap_bottom < overlap_top:
                    self.position.y = wall.bottom  # Push down
                    self.velocity.y = 0

    def enter_house(self, house):
        print(f"DETECTING DOOR THAT NEEDS TO BE REMOVED FROM COLLIDING {house.entrance_side}!")
        return vector(random.randint(self.rect.left, self.rect.right - 25),
                      random.randint(self.rect.top, self.rect.bottom - 25))
        
    def draw_stats(self):
        x_pos_text = self.font.render(f'X: {int(self.position.x)}', True, WHITE)
        y_pos_text = self.font.render(f'Y: {int(self.position.y)}', True, WHITE)
        health_text = self.font.render(f'Health: {self.health}', True, WHITE)
        damage_text = self.font.render(f'Damage: {self.damage}', True, WHITE)
        speed_text = self.font.render(f'Speed: {self.speed}', True, WHITE)
        
        self.display.blit(x_pos_text, (10, 10))
        self.display.blit(y_pos_text, (10, 40))
        self.display.blit(health_text, (10, 70))
        self.display.blit(damage_text, (10, 100))
        self.display.blit(speed_text, (10, 130))

class Archer(Player):
    def __init__(self, display):
        super().__init__(display, BLUE)
        self.speed += 30
        self.damage = 5

class Warlock(Player):
    def __init__(self, display):
        super().__init__(display, GREEN)
        self.health += 20
        self.damage = 10

class Game:
    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont("arial", 25, bold=True)
        self.frame = pygame.time.Clock()
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("DEMO2")
        self.running = True
        self.game_state = "MENU"
        self.player = None
        self.houses = pygame.sprite.Group()
        self.map_level = None
        pygame.mouse.set_visible(False)  # Hide the mouse cursor
        self.map_level = Map_Level(2500, 2500, 20)

    def check_overlap(self, new_house):
        for house in self.houses:
            if new_house.rect.colliderect(house.rect):
                return True
        return False

    def run_game(self):
        while self.running:
            dt = self.frame.tick(FPS) / 1000  # Delta time
            if self.game_state == "MENU":
                self.handle_menu_events()
                self.draw_menu()
            elif self.game_state == "PLAY":
                self.handle_game_events()
                self.update_game(dt)
                self.draw_game()
            elif self.game_state == "PAUSE":
                self.handle_pause_events()
                self.draw_pause()
        pygame.quit()
        sys.exit(1)

    def handle_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Select Archer
                    self.player = Archer(self.display)
                    self.game_state = "PLAY"
                elif event.key == pygame.K_2:  # Select Warlock
                    self.player = Warlock(self.display)
                    self.game_state = "PLAY"

    def draw_menu(self):
        self.display.fill(BLACK)
        title = self.font.render("Select Your Character", True, GREEN)
        self.display.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))

        archer_text = self.font.render("Press 1 for Archer", True, GREEN)
        self.display.blit(archer_text, (WIDTH // 2 - archer_text.get_width() // 2, HEIGHT // 2))

        warlock_text = self.font.render("Press 2 for Warlock", True, GREEN)
        self.display.blit(warlock_text, (WIDTH // 2 - warlock_text.get_width() // 2, HEIGHT // 2 + 30))
        pygame.display.flip()

    def handle_game_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Pause the game
                    self.game_state = "PAUSE"

    def draw_game(self):
        self.display.fill(BLACK)
        camera_offset_x = max(0, min(self.player.position.x - WIDTH // 2, self.map_level.width - WIDTH))
        camera_offset_y = max(0, min(self.player.position.y - HEIGHT // 2, self.map_level.height - HEIGHT))
        camera_offset = vector(-camera_offset_x, -camera_offset_y)
        self.map_level.draw_map(self.display, camera_offset)
        self.player.draw_player(camera_offset)
        self.player.draw_stats()
        fps_text = self.font.render(f'FPS: {int(self.frame.get_fps())}', True, WHITE)
        self.display.blit(fps_text, (10, 160))
        
        # Draw trigger rectangle following the mouse
        mouse_pos = pygame.mouse.get_pos()
        trigger_rect = pygame.Rect(mouse_pos[0] - 25 // 2, mouse_pos[1] - 25 // 2, 12, 12)
        pygame.draw.rect(self.display, (255, 0, 0), trigger_rect, 2)  # Red rectangle with 2px border

        pygame.display.flip()

    def update_game(self, dt):
        self.player.update_player(dt, self.map_level.houses)

    def handle_pause_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Resume the game
                    self.game_state = "PLAY"

    def draw_pause(self):
        self.display.fill(BLACK)
        pause_text = self.font.render("Game Paused", True, GREEN)
        self.display.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 4))

        resume_text = self.font.render("Press R to Resume", True, GREEN)
        self.display.blit(resume_text, (WIDTH // 2 - resume_text.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run_game()
