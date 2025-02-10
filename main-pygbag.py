from data.ball import Ball
from data.board import *
from data.goal import *
from data.settings import *
import os, pygame, pymunk, random, asyncio

# Force Pure Python mode for Pymunk (avoids CFFI issues)
os.environ["PYMUNK_NO_CFFI"] = "1"

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE_STRING)
        self.clock = pygame.time.Clock()
        self.delta_time = 0

        # Pymunk
        self.space = pymunk.Space()
        self.space.gravity = (0, 1800)

        # Plinko setup
        self.ball_group = pygame.sprite.Group()
        self.board = Board(self.space)

        # Load audio safely for the web
        try:
            pygame.mixer.init()
            self.bgm = pygame.mixer.music
            self.bgm.load("audio/boba date.ogg")
            self.bgm.play(-1)
            self.bgm.set_volume(0.2)
        except pygame.error:
            print("⚠️ Audio failed to load. Running without music.")

    async def main(self):
        self.start_time = pygame.time.get_ticks()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if self.board.handle_clear_button(mouse_pos):
                        prev_multi_group.empty()
                        self.ball_group.empty()

                    elif self.board.handle_drop_button(mouse_pos):
                        random_x = WIDTH // 2 + random.choice([random.randint(-20, -1), random.randint(1, 20)])
                        self.ball = Ball((random_x, 250), self.space, self.board, self.delta_time)
                        self.ball_group.add(self.ball)
                        self.board.pressing_play = False

            self.screen.fill(BG_COLOR)

            # Time variables
            self.delta_time = self.clock.tick(FPS) / 1000.0

            # Pymunk
            self.space.step(self.delta_time)
            self.board.update()
            self.ball_group.update()

            pygame.display.update()
            await asyncio.sleep(0)  # Allow async execution in the browser

        pygame.quit()

# Ensure the game runs properly in Pygbag
game = Game()
asyncio.run(game.main())
