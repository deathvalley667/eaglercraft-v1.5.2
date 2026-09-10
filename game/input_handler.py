"""
Input handler - manages keyboard, mouse, and gamepad input
"""

import pygame

class InputHandler:
    def __init__(self):
        self.keys_pressed = set()
        self.mouse_pressed = set()
        self.mouse_pos = (0, 0)
        self.scroll_direction = 0
    
    def handle_event(self, event):
        """Handle pygame events"""
        if event.type == pygame.KEYDOWN:
            self.keys_pressed.add(event.key)
        elif event.type == pygame.KEYUP:
            self.keys_pressed.discard(event.key)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_pressed.add(event.button)
            if event.button == 4:  # Scroll up
                self.scroll_direction = 1
            elif event.button == 5:  # Scroll down
                self.scroll_direction = -1
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_pressed.discard(event.button)
        elif event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
    
    def is_key_pressed(self, key):
        """Check if key is currently pressed"""
        return key in self.keys_pressed
    
    def is_mouse_pressed(self, button):
        """Check if mouse button is pressed"""
        return button in self.mouse_pressed
    
    def get_mouse_pos(self):
        """Get current mouse position"""
        return self.mouse_pos
    
    def clear_scroll(self):
        """Clear scroll direction"""
        self.scroll_direction = 0
