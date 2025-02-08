from ball import Ball
from board import *
from goal import *
from settings import *
import ctypes, pygame, pymunk, random, asyncio

# Maintain resolution regardless of Windows scaling settings
# ctypes.windll.user32.SetProcessDPIAware()

class Game:
    def __init__(self):
        # General setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE_STRING)
        self.clock = pygame.time.Clock()
        self.delta_time = 0
        pygame.mixer.init()

        # Pymunk
        self.space = pymunk.Space()
        self.space.gravity = (0, 1800)

        # Plinko setup
        self.ball_group = pygame.sprite.Group()
        self.board = Board(self.space)

        # bgm
        pygame.mixer.music.load("audio/boba date.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)

    async def main(self):
        self.start_time = pygame.time.get_ticks()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False  # Do not use sys.exit() in web environments
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Check for clear button click
                    if self.board.handle_clear_button(mouse_pos):
                        prev_multi_group.empty()  # Clear the score history

                    # Check for drop button click
                    elif self.board.handle_drop_button(mouse_pos):
                        random_x = WIDTH // 2 + random.choice([random.randint(-20, -1), random.randint(1, 20)])
                        self.ball = Ball((random_x, 250), self.space, self.board, self.delta_time)
                        self.ball_group.add(self.ball)
                        self.board.pressing_play = False
                                             
                elif event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    self.board.handle_clear_button(mouse_pos)
                    self.board.handle_drop_button(mouse_pos)

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

if __name__ == '__main__':
    game = Game()
    asyncio.run(game.main())  # Use asyncio.run() to make it web-compatible