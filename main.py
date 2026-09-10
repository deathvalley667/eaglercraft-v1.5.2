"""
Eaglercraft v1.5.2 - A Minecraft-inspired game engine
Main entry point for the game
"""

import pygame
import sys
from game.engine import GameEngine
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE, FPS

def main():
    # Initialize Pygame
    pygame.init()
    
    # Create the game engine
    game = GameEngine(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE, FPS)
    
    # Run the game loop
    game.run()
    
    # Cleanup
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
