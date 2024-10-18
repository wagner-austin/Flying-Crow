import pygame
import os
import random

# Initialize pygame
pygame.init()

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAVITY = 0.4
JUMP_STRENGTH = -17
FLOOR_Y = 2110
BACKGROUND_SCROLL_SPEED = 8
CLOUD_SCROLL_SPEED = 4
FLYING_ANIMATION_SPEED = 5
WALKING_ANIMATION_SPEED = 9
MAX_CLOUDS = 8
MENU_BACKGROUND_SCROLL_SPEED = 2

# Asset paths
# Get the absolute path to the folder where the script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_FOLDER = os.path.join(BASE_DIR, "assets")  # Use relative path

CROW_WALK_ANIMATION_SHEET_PATH = os.path.join(ASSET_FOLDER, "crow_walk.png")
CROW_FLYING_ANIMATION_SHEET_PATH = os.path.join(ASSET_FOLDER, "crow_flying_animation_sheet.png")
BACKGROUND_IMAGE_PATH = os.path.join(ASSET_FOLDER, "background.png")
CLOUD_IMAGE_PATH = os.path.join(ASSET_FOLDER, "cloud.png")
START_BUTTON_IMAGE_PATH = os.path.join(ASSET_FOLDER, "start_button.png")
PAUSE_BUTTON_IMAGE_PATH = os.path.join(ASSET_FOLDER, "pause_button.png")
RESUME_BUTTON_IMAGE_PATH = os.path.join(ASSET_FOLDER, "resume_button.png")
RESTART_BUTTON_IMAGE_PATH = os.path.join(ASSET_FOLDER, "restart_button.png")
MENU_BUTTON_IMAGE_PATH = os.path.join(ASSET_FOLDER, "menu_button.png")
GAME_TITLE_IMAGE_PATHS = [
    os.path.join(ASSET_FOLDER, f"game_title{i}.png") for i in range(1, 4)
]

def load_specific_frames_from_sheet(sheet, frame_positions, frame_width, frame_height):
    return [sheet.subsurface(pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height))
            for col, row in frame_positions]

class Cloud(pygame.sprite.Sprite):
    def __init__(self, image, screen_width):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.screen_width = screen_width
        self.rect.x = random.randint(self.screen_width, self.screen_width + 500)
        self.rect.y = random.randint(50, 800)

    def update(self):
        self.rect.x -= CLOUD_SCROLL_SPEED
        if self.rect.x < -self.rect.width:
            self.kill()

class Crow(pygame.sprite.Sprite):
    def __init__(self, walking_frames, flying_frames):
        super().__init__()
        self.walking_frames = walking_frames
        self.flying_frames = flying_frames
        self.image = self.walking_frames[0]
        self.rect = self.image.get_rect(x=700, y=1000)
        self.velocity_y = 0
        self.on_ground = True
        self.frame_counter = 0

    def update(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        if self.rect.y >= FLOOR_Y:
            self.rect.y = FLOOR_Y
            self.velocity_y = 0
            self.on_ground = True
            self.animate(self.walking_frames, WALKING_ANIMATION_SPEED)
        else:
            self.on_ground = False
            self.animate(self.flying_frames, FLYING_ANIMATION_SPEED)

    def animate(self, frames, animation_speed):
        self.frame_counter = (self.frame_counter + 1) % (animation_speed * len(frames))
        frame_index = self.frame_counter // animation_speed
        self.image = frames[frame_index]

    def jump(self):
        self.velocity_y = JUMP_STRENGTH

class Button(pygame.sprite.Sprite):
    def __init__(self, image, position, action):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=position)
        self.action = action

    def check_for_input(self, position):
        if self.rect.collidepoint(position):
            self.action()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class GameState:
    MENU = 'menu'
    RUNNING = 'running'
    PAUSED = 'paused'
    GAME_OVER = 'game_over'

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Side-view Crow Jump")
        self.screen_width, self.screen_height = self.screen.get_size()
        self.load_assets()
        self.initialize_game()
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.MENU
        self.title_animation_index = 0
        self.title_last_update = pygame.time.get_ticks()
        self.title_animation_speed = 500
        self.background_x = 0

    def load_assets(self):
        self.background = pygame.transform.scale(
            pygame.image.load(BACKGROUND_IMAGE_PATH).convert(),
            (self.screen_width, self.screen_height)
        )
        self.cloud_image = pygame.transform.scale(
            pygame.image.load(CLOUD_IMAGE_PATH).convert_alpha(), (600, 300)
        )
        # Load crow animations
        self.crow_flying_frames = self.load_crow_frames(
            CROW_FLYING_ANIMATION_SHEET_PATH, 5, 2, (200, 200)
        )
        self.crow_walk_frames = self.load_crow_frames(
            CROW_WALK_ANIMATION_SHEET_PATH, 3, 3, (185, 185),
            [(col, row) for row in [0, 2] for col in range(3)]
        )
        # Load buttons
        button_info = [
            ('start_button', START_BUTTON_IMAGE_PATH, (500, 200)),
            ('pause_button', PAUSE_BUTTON_IMAGE_PATH, (400, 150)),
            ('resume_button', RESUME_BUTTON_IMAGE_PATH, (400, 150)),
            ('restart_button', RESTART_BUTTON_IMAGE_PATH, (400, 150)),
            ('menu_button', MENU_BUTTON_IMAGE_PATH, (400, 150)),
        ]
        self.button_images = {
            name: pygame.transform.scale(
                pygame.image.load(path).convert_alpha(), size
            ) for name, path, size in button_info
        }
        # Load game title images
        self.game_title_images = [
            pygame.transform.scale(
                pygame.image.load(path).convert_alpha(), (800, 400)
            ) for path in GAME_TITLE_IMAGE_PATHS
        ]

    def load_crow_frames(self, sheet_path, cols, rows, size, positions=None):
        sheet = pygame.image.load(sheet_path).convert_alpha()
        frame_width = sheet.get_width() // cols
        frame_height = sheet.get_height() // rows
        if positions is None:
            positions = [(col, row) for row in range(rows) for col in range(cols)]
        frames = load_specific_frames_from_sheet(
            sheet, positions, frame_width, frame_height
        )
        return [pygame.transform.scale(frame, size) for frame in frames]

    def initialize_game(self):
        self.all_sprites = pygame.sprite.Group()
        self.block = Crow(self.crow_walk_frames, self.crow_flying_frames)
        self.all_sprites.add(self.block)
        self.clouds = pygame.sprite.Group()
        self.last_cloud_spawn_time = 0
        self.cloud_spawn_delay = random.uniform(3500, 5000)
        # Initialize buttons
        self.buttons = {}
        positions = {
            'pause_button': (self.screen_width - 240, 100),
            'resume_button': (self.screen_width / 2, self.screen_height / 2 - 150),
            'restart_button': (self.screen_width / 2, self.screen_height / 2 + 50),
            'menu_button': (self.screen_width / 2, self.screen_height / 2 + 250),
            'start_button': (self.screen_width / 2, self.screen_height / 2 + 100),
        }
        actions = {
            'pause_button': self.pause_game,
            'resume_button': self.resume_game,
            'restart_button': self.restart,
            'menu_button': self.go_to_menu,
            'start_button': self.start_game,
        }
        for name, image in self.button_images.items():
            self.buttons[name] = Button(image, positions[name], actions[name])
        self.title_animation_index = 0
        self.title_last_update = pygame.time.get_ticks()

    def run(self):
        while self.running:
            self.handle_events()
            if self.state == GameState.RUNNING:
                self.update_game()
            elif self.state == GameState.MENU:
                self.update_menu_screen()
            self.draw()
            self.clock.tick(60)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type in [pygame.QUIT, pygame.KEYDOWN] and event.key == pygame.K_ESCAPE:
                self.running = False
            if event.type in [pygame.FINGERDOWN, pygame.MOUSEBUTTONDOWN]:
                x, y = self.get_touch_position(event)
                for button in self.get_active_buttons():
                    if button.rect.collidepoint(x, y):
                        button.check_for_input((x, y))
                        break
                else:
                    if self.state == GameState.RUNNING:
                        self.block.jump()

    def get_touch_position(self, event):
        if event.type == pygame.FINGERDOWN:
            x = int(event.x * self.screen_width)
            y = int(event.y * self.screen_height)
        else:
            x, y = event.pos
        return x, y

    def update_game(self):
        self.background_x = (self.background_x - BACKGROUND_SCROLL_SPEED) % self.screen_width
        self.all_sprites.update()
        self.clouds.update()
        self.spawn_clouds()

    def update_menu_screen(self):
        self.background_x = (self.background_x - MENU_BACKGROUND_SCROLL_SPEED) % self.screen_width
        now = pygame.time.get_ticks()
        if now - self.title_last_update > self.title_animation_speed:
            self.title_last_update = now
            self.title_animation_index = (self.title_animation_index + 1) % len(self.game_title_images)

    def spawn_clouds(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_cloud_spawn_time >= self.cloud_spawn_delay and len(self.clouds) < MAX_CLOUDS:
            cloud = Cloud(self.cloud_image, self.screen_width)
            self.clouds.add(cloud)
            self.last_cloud_spawn_time = current_time
            self.cloud_spawn_delay = random.uniform(3500, 5000)

    def draw(self):
        self.screen.blit(self.background, (self.background_x - self.screen_width, 0))
        self.screen.blit(self.background, (self.background_x, 0))
        if self.state == GameState.RUNNING:
            self.draw_game()
            self.buttons['pause_button'].draw(self.screen)
        elif self.state == GameState.PAUSED:
            self.draw_game()
            self.draw_overlay("Paused")
        elif self.state == GameState.MENU:
            self.draw_menu_screen()
        elif self.state == GameState.GAME_OVER:
            self.draw_overlay("Game Over")
        pygame.display.flip()

    def draw_game(self):
        self.all_sprites.draw(self.screen)
        self.clouds.draw(self.screen)

    def draw_overlay(self, text):
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        font = pygame.font.SysFont(None, 150)
        text_surf = font.render(text, True, WHITE)
        text_rect = text_surf.get_rect(center=(self.screen_width / 2, self.screen_height / 2 - 350))
        self.screen.blit(text_surf, text_rect)
        for button in self.get_active_buttons():
            button.draw(self.screen)

    def draw_menu_screen(self):
        self.draw_game()
        current_title_image = self.game_title_images[self.title_animation_index]
        title_rect = current_title_image.get_rect(center=(self.screen_width / 2, self.screen_height / 2 - 200))
        self.screen.blit(current_title_image, title_rect)
        self.buttons['start_button'].draw(self.screen)

    def get_active_buttons(self):
        if self.state == GameState.MENU:
            return [self.buttons['start_button']]
        elif self.state == GameState.RUNNING:
            return [self.buttons['pause_button']]
        elif self.state == GameState.PAUSED:
            return [self.buttons['resume_button'], self.buttons['restart_button'], self.buttons['menu_button']]
        elif self.state == GameState.GAME_OVER:
            return [self.buttons['restart_button'], self.buttons['menu_button']]
        return []

    def pause_game(self):
        self.state = GameState.PAUSED

    def resume_game(self):
        self.state = GameState.RUNNING

    def go_to_menu(self):
        self.initialize_game()
        self.state = GameState.MENU

    def restart(self):
        self.initialize_game()
        self.state = GameState.RUNNING

    def start_game(self):
        self.initialize_game()
        self.state = GameState.RUNNING

if __name__ == "__main__":
    game = Game()
    game.run()
