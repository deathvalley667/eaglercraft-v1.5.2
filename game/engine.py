"""
Main game engine - handles game loop, rendering, and updates
"""

import pygame
import numpy as np
from game.world import World
from game.player import Player
from game.renderer import Renderer
from game.input_handler import InputHandler
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COLOR_SKY

class GameEngine:
    def __init__(self, width, height, title, fps):
        self.width = width
        self.height = height
        self.title = title
        self.fps = fps
        self.clock = pygame.time.Clock()
        
        # Initialize display
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        
        # Initialize game systems
        self.world = World()
        self.player = Player()
        self.renderer = Renderer(self.screen, width, height)
        self.input_handler = InputHandler()
        
        self.running = True
        self.paused = False
        
    def handle_events(self):
        """Handle input and window events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
            
            # Pass event to input handler
            self.input_handler.handle_event(event)
    
    def update(self, dt):
        """Update game logic"""
        if self.paused:
            return
        
        # Get player input
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        
        # Update player
        self.player.update(keys, mouse_buttons, self.world, dt)
        
        # Update world (could include block updates, etc.)
        self.world.update(dt)
    
    def render(self):
        """Render the game"""
        # Clear screen
        self.screen.fill(COLOR_SKY)
        
        # Render world and player
        self.renderer.render(self.world, self.player)
        
        # Render UI
        self.renderer.render_ui(self.paused)
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(self.fps) / 1000.0  # Delta time in seconds
            
            self.handle_events()
            self.update(dt)
            self.render()
