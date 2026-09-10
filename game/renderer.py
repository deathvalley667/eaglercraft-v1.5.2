"""
Rendering system - handles all drawing and visualization
Uses simple 2.5D isometric rendering for Minecraft-style view
"""

import pygame
import numpy as np
from config import (
    BLOCK_SIZE, COLOR_SKY, COLOR_GRASS, COLOR_DIRT, COLOR_STONE,
    COLOR_WATER, COLOR_SAND, COLOR_WHITE, COLOR_BLACK, BLOCK_TYPES
)

class Renderer:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font_small = pygame.font.Font(None, 24)
        self.font_large = pygame.font.Font(None, 36)
    
    def render(self, world, player):
        """Render world and player view"""
        # Render 3D world using simple projection
        self._render_world(world, player)
    
    def _render_world(self, world, player):
        """Render visible world chunks"""
        # Get visible chunks
        visible_chunks = world.get_visible_chunks(player.pos)
        
        # Draw all blocks in visible chunks
        for chunk in visible_chunks:
            if not chunk.generated:
                continue
            
            # Draw blocks
            for bx in range(16):
                for by in range(0, min(chunk.blocks.shape[1], 128), 1):
                    for bz in range(16):
                        block_type = chunk.blocks[bx, by, bz]
                        
                        if block_type == 0:  # Skip air
                            continue
                        
                        # Calculate world position
                        world_x = chunk.x * 16 + bx
                        world_y = by
                        world_z = chunk.z * 16 + bz
                        
                        # Project to screen
                        screen_pos = self._project_to_screen(
                            np.array([world_x, world_y, world_z], dtype=np.float32),
                            player
                        )
                        
                        if screen_pos is None:
                            continue
                        
                        # Draw block
                        self._draw_block(block_type, screen_pos)
    
    def _project_to_screen(self, world_pos, player):
        """Project 3D world position to 2D screen using player camera"""
        # Translate to camera space
        relative_pos = world_pos - player.get_eye_pos()
        
        # Rotate based on player rotation
        pitch = np.radians(player.pitch)
        yaw = np.radians(player.yaw)
        
        # Rotation matrices
        cos_p, sin_p = np.cos(pitch), np.sin(pitch)
        cos_y, sin_y = np.cos(yaw), np.sin(yaw)
        
        # Apply yaw rotation (Y axis)
        x = relative_pos[0] * cos_y - relative_pos[2] * sin_y
        z = relative_pos[0] * sin_y + relative_pos[2] * cos_y
        
        # Apply pitch rotation (X axis)
        y = relative_pos[1] * cos_p - z * sin_p
        z = relative_pos[1] * sin_p + z * cos_p
        
        # Project to screen
        if z <= 0.1:  # Behind camera
            return None
        
        # Perspective projection
        fov_rad = np.radians(70)
        focal_length = (self.width / 2) / np.tan(fov_rad / 2)
        
        screen_x = self.width / 2 + (x / z) * focal_length
        screen_y = self.height / 2 - (y / z) * focal_length
        
        # Check if on screen
        if screen_x < -50 or screen_x > self.width + 50 or \
           screen_y < -50 or screen_y > self.height + 50:
            return None
        
        return (screen_x, screen_y, z)
    
    def _draw_block(self, block_type, screen_info):
        """Draw a block at screen position"""
        screen_x, screen_y, depth = screen_info
        
        # Scale block size based on distance
        block_size = max(2, int(BLOCK_SIZE / (depth + 1)))
        
        # Select color based on block type
        color = self._get_block_color(block_type)
        
        # Add shading based on depth
        shading = max(0.3, 1.0 - depth / 200)
        color = tuple(int(c * shading) for c in color)
        
        # Draw block
        rect = pygame.Rect(
            screen_x - block_size / 2,
            screen_y - block_size / 2,
            block_size,
            block_size
        )
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, COLOR_BLACK, rect, 1)
    
    def _get_block_color(self, block_type):
        """Get color for block type"""
        colors = {
            1: COLOR_STONE,
            2: COLOR_GRASS,
            3: COLOR_DIRT,
            4: (112, 112, 112),  # Cobblestone
            5: (139, 90, 43),    # Log
            6: (34, 139, 34),    # Leaves
            7: COLOR_SAND,
            8: (192, 192, 192),  # Gravel
            9: COLOR_WATER,
            10: (255, 69, 0),    # Lava
        }
        return colors.get(block_type, COLOR_GRASS)
    
    def render_ui(self, paused):
        """Render user interface overlay"""
        # Render crosshair
        center_x, center_y = self.width // 2, self.height // 2
        pygame.draw.line(self.screen, COLOR_WHITE, (center_x - 10, center_y), (center_x + 10, center_y), 2)
        pygame.draw.line(self.screen, COLOR_WHITE, (center_x, center_y - 10), (center_x, center_y + 10), 2)
        
        # Render pause menu if paused
        if paused:
            self._render_pause_menu()
        
        # Render HUD
        self._render_hud()
    
    def _render_pause_menu(self):
        """Render pause menu"""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(128)
        overlay.fill(COLOR_BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = self.font_large.render("PAUSED", True, COLOR_WHITE)
        pause_rect = pause_text.get_rect(center=(self.width // 2, self.height // 2 - 50))
        self.screen.blit(pause_text, pause_rect)
        
        # Resume instruction
        resume_text = self.font_small.render("Press P to resume", True, COLOR_WHITE)
        resume_rect = resume_text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(resume_text, resume_rect)
    
    def _render_hud(self):
        """Render heads-up display"""
        # FPS
        fps_text = self.font_small.render("Eaglercraft v1.5.2", True, COLOR_WHITE)
        self.screen.blit(fps_text, (10, 10))
