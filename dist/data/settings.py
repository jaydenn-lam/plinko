import ctypes, pygame, pymunk

TITLE_STRING = 'Digisoc Boba Plinko'
FPS = 60

# Maintain resolution regardless of Windows scaling settings
# ctypes.windll.user32.SetProcessDPIAware()

WIDTH = 1920
HEIGHT = 1080

# Plinko config
BG_COLOR = (255, 243, 234)
BROWN = (122, 73, 32)  
DARK_BROWN = (101, 67, 33)
MILK_TEA = (222, 184, 135)
STRAW = (235, 211, 170)
MULTI_HEIGHT = int(HEIGHT / 19) # 56 on 1920x1080
MULTI_COLLISION = HEIGHT - (MULTI_HEIGHT * 2) # 968 on 1920x1080

SCORE_RECT = int(WIDTH / 16) # 120 on 1920x1080

OBSTACLE_COLOR = "White"
OBSTACLE_RAD = int(WIDTH / 240) # 8 on 1920x1080
OBSTACLE_PAD = int(HEIGHT / 19) # 56 on 1920x1080
OBSTACLE_START = (int((WIDTH / 2) - OBSTACLE_PAD), int((HEIGHT - (HEIGHT * .7)))) # (904, 108) on 1920x1080
segmentA_2 = OBSTACLE_START

BALL_RAD = 16

# Dictionary to keep track of scores
multipliers = {
    "1000": 0,
    "130": 0,
    "26": 0,
    "9": 0,
    "4": 0,
    "2": 0,
    "0.2": 0
}

# RGB Values for multipliers
multi_rgb = {
    (0, 1000): (255, 255, 255),
    (1, 130): (255, 255, 255),
    (2, 26): (255, 255, 255),
    (3, 9): (255, 255, 255),
    (8, 0.2): (107, 74, 213),
    (13, 9): (255, 255, 255),
    (14, 26): (255, 255, 255),
    (15, 130): (255, 255, 255),
    (16, 1000): (255, 255, 255),
}

# Number of multipliers shown underneath obstacles
NUM_MULTIS = 9

# Pymunk settings (prevent same class collisions)
BALL_CATEGORY = 1
OBSTACLE_CATEGORY = 2
BALL_MASK = pymunk.ShapeFilter.ALL_MASKS() ^ BALL_CATEGORY
OBSTACLE_MASK = pymunk.ShapeFilter.ALL_MASKS()

# Audio stuff
pygame.mixer.init()
click = pygame.mixer.Sound("audio/click.mp3")
sound01 = pygame.mixer.Sound("audio/win-ding.mp3")
sound01.set_volume(0.7)
sound02 = pygame.mixer.Sound("audio/lose-ding.mp3")
sound02.set_volume(1)
sound03 = pygame.mixer.Sound("audio/lose-ding.mp3")
sound03.set_volume(1)
sound04 = pygame.mixer.Sound("audio/lose-ding.mp3")
sound04.set_volume(1)
sound05 = pygame.mixer.Sound("audio/lose-ding.mp3")
sound05.set_volume(1)
sound06 = pygame.mixer.Sound("audio/lose-ding.mp3")
sound06.set_volume(1)
sound07 = pygame.mixer.Sound("audio/lose-ding.mp3")
sound07.set_volume(1)