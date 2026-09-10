"""
Player entity - handles player position, movement, and interaction
"""

import pygame
import numpy as np
from config import (
    PLAYER_SPEED, PLAYER_JUMP_FORCE, GRAVITY, REACH_DISTANCE,
    CAMERA_SENSITIVITY, PLAYER_HEIGHT, PLAYER_WIDTH
)

class Player:
    def __init__(self):
        # Position (x, y, z)
        self.pos = np.array([8.0, 65.0, 8.0], dtype=np.float32)
        
        # Velocity
        self.vel = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        
        # Rotation (pitch, yaw)
        self.pitch = 0.0
        self.yaw = 0.0
        
        # State
        self.on_ground = False
        self.flying = False
        self.health = 20
        self.hunger = 20
        self.inventory = {}
        self.selected_item = 1  # Stone
        
        # Eye height
        self.eye_height = PLAYER_HEIGHT * 0.9
    
    def update(self, keys, mouse_buttons, world, dt):
        """Update player state"""
        # Handle movement input
        self._handle_movement(keys, dt)
        
        # Apply gravity
        self._apply_physics(world, dt)
        
        # Handle mouse input (camera rotation)
        self._handle_camera()
        
        # Handle block breaking/placing
        self._handle_interactions(mouse_buttons, world)
        
        # Update position based on velocity
        self._update_position(world, dt)
    
    def _handle_movement(self, keys, dt):
        """Handle WASD movement input"""
        move_dir = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        
        # Forward/backward
        if keys[pygame.K_w]:
            move_dir[0] += np.sin(np.radians(self.yaw))
            move_dir[2] += np.cos(np.radians(self.yaw))
        if keys[pygame.K_s]:
            move_dir[0] -= np.sin(np.radians(self.yaw))
            move_dir[2] -= np.cos(np.radians(self.yaw))
        
        # Left/right (strafe)
        if keys[pygame.K_a]:
            move_dir[0] -= np.cos(np.radians(self.yaw))
            move_dir[2] += np.sin(np.radians(self.yaw))
        if keys[pygame.K_d]:
            move_dir[0] += np.cos(np.radians(self.yaw))
            move_dir[2] -= np.sin(np.radians(self.yaw))
        
        # Jump
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel[1] = PLAYER_JUMP_FORCE
            self.on_ground = False
        
        # Flying mode toggle
        if keys[pygame.K_f]:
            self.flying = not self.flying
        
        # Normalize and apply speed
        if np.linalg.norm(move_dir) > 0:
            move_dir = move_dir / np.linalg.norm(move_dir)
            self.vel[0] = move_dir[0] * PLAYER_SPEED
            self.vel[2] = move_dir[2] * PLAYER_SPEED
        else:
            self.vel[0] *= 0.9
            self.vel[2] *= 0.9
        
        # Flying vertical movement
        if self.flying:
            if keys[pygame.K_SPACE]:
                self.vel[1] = PLAYER_SPEED
            elif keys[pygame.K_LSHIFT]:
                self.vel[1] = -PLAYER_SPEED
            else:
                self.vel[1] = 0
    
    def _apply_physics(self, world, dt):
        """Apply gravity and collision physics"""
        if not self.flying:
            # Apply gravity
            self.vel[1] -= GRAVITY * dt * 10
            
            # Terminal velocity
            self.vel[1] = max(self.vel[1], -20)
        
        # Check ground collision
        self.on_ground = False
        if not self.flying:
            check_pos = self.pos.copy()
            check_pos[1] -= 0.1
            if world.is_solid(check_pos[0], check_pos[1], check_pos[2]):
                self.on_ground = True
                self.vel[1] = 0
    
    def _update_position(self, world, dt):
        """Update position with collision detection"""
        new_pos = self.pos + self.vel * dt
        
        # Simple AABB collision detection
        collision_dist = PLAYER_WIDTH / 2
        
        # Check collision and adjust position
        for axis in range(3):
            test_pos = self.pos.copy()
            test_pos[axis] = new_pos[axis]
            
            # Check multiple points for collision
            hit = False
            for dx in [-collision_dist, 0, collision_dist]:
                for dz in [-collision_dist, 0, collision_dist]:
                    check_x = test_pos[0] + dx
                    check_y = test_pos[1]
                    check_z = test_pos[2] + dz
                    
                    if world.is_solid(check_x, check_y, check_z):
                        hit = True
                        break
            
            if not hit:
                self.pos[axis] = new_pos[axis]
            else:
                self.vel[axis] = 0
    
    def _handle_camera(self):
        """Handle camera rotation with mouse"""
        if pygame.mouse.get_focused():
            mouse_rel = pygame.mouse.get_rel()
            
            self.yaw -= mouse_rel[0] * CAMERA_SENSITIVITY
            self.pitch += mouse_rel[1] * CAMERA_SENSITIVITY
            
            # Clamp pitch
            self.pitch = max(-89, min(89, self.pitch))
            
            # Wrap yaw
            self.yaw = self.yaw % 360
    
    def _handle_interactions(self, mouse_buttons, world):
        """Handle block breaking and placing"""
        # This will be implemented in the interaction system
        pass
    
    def get_eye_pos(self):
        """Get position of player's eyes"""
        return self.pos + np.array([0, self.eye_height, 0])
    
    def get_look_vector(self):
        """Get normalized direction player is looking"""
        pitch_rad = np.radians(self.pitch)
        yaw_rad = np.radians(self.yaw)
        
        x = np.sin(yaw_rad) * np.cos(pitch_rad)
        y = -np.sin(pitch_rad)
        z = np.cos(yaw_rad) * np.cos(pitch_rad)
        
        return np.array([x, y, z])
