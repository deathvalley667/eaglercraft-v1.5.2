"""
Game configuration and constants
"""

# Screen settings
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
GAME_TITLE = "Eaglercraft v1.5.2"
FPS = 60

# World settings
CHUNK_SIZE = 16
WORLD_HEIGHT = 256
RENDER_DISTANCE = 8

# Block settings
BLOCK_SIZE = 32
BLOCK_TYPES = {
    0: "air",
    1: "stone",
    2: "grass",
    3: "dirt",
    4: "cobblestone",
    5: "oak_log",
    6: "oak_leaves",
    7: "sand",
    8: "gravel",
    9: "water",
    10: "lava",
}

# Player settings
PLAYER_HEIGHT = 1.8
PLAYER_WIDTH = 0.6
PLAYER_SPEED = 5
PLAYER_JUMP_FORCE = 15
GRAVITY = 0.98
REACH_DISTANCE = 5

# Camera settings
FOV = 70
CAMERA_SENSITIVITY = 0.1

# Colors
COLOR_SKY = (135, 206, 235)
COLOR_GRASS = (34, 139, 34)
COLOR_DIRT = (139, 90, 43)
COLOR_STONE = (128, 128, 128)
COLOR_WATER = (0, 119, 182)
COLOR_SAND = (238, 214, 175)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
