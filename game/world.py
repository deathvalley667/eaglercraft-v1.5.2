"""
World generation and management
Handles chunks, blocks, and world data
"""

import numpy as np
import random
from config import CHUNK_SIZE, WORLD_HEIGHT, BLOCK_SIZE

class Chunk:
    """Represents a 16x256x16 chunk of blocks"""
    def __init__(self, x, z):
        self.x = x
        self.z = z
        # 16x256x16 chunk (width x height x depth)
        self.blocks = np.zeros((CHUNK_SIZE, WORLD_HEIGHT, CHUNK_SIZE), dtype=np.uint8)
        self.generated = False
        self.mesh_dirty = True
    
    def generate(self):
        """Generate terrain for this chunk"""
        if self.generated:
            return
        
        # Simple noise-based terrain generation
        for bx in range(CHUNK_SIZE):
            for bz in range(CHUNK_SIZE):
                # Base terrain height (hills)
                height = self._get_height(bx, bz)
                
                # Fill blocks
                for by in range(int(height)):
                    if by < int(height) - 3:
                        self.blocks[bx, by, bz] = 1  # Stone
                    elif by < int(height) - 1:
                        self.blocks[bx, by, bz] = 3  # Dirt
                    else:
                        self.blocks[bx, by, bz] = 2  # Grass
        
        self.generated = True
        self.mesh_dirty = True
    
    def _get_height(self, x, z):
        """Generate height at position using simple noise"""
        # Simple Perlin-like noise simulation
        wx = self.x * CHUNK_SIZE + x
        wz = self.z * CHUNK_SIZE + z
        
        # Multiple layers of noise for natural terrain
        height = 64
        height += 20 * np.sin(wx / 50) * np.cos(wz / 50)
        height += 10 * np.sin(wx / 20) * np.cos(wz / 20)
        height += 5 * random.random()
        
        return max(1, min(int(height), WORLD_HEIGHT - 1))
    
    def set_block(self, x, y, z, block_type):
        """Set block at position"""
        if 0 <= x < CHUNK_SIZE and 0 <= y < WORLD_HEIGHT and 0 <= z < CHUNK_SIZE:
            self.blocks[x, y, z] = block_type
            self.mesh_dirty = True
    
    def get_block(self, x, y, z):
        """Get block type at position"""
        if 0 <= x < CHUNK_SIZE and 0 <= y < WORLD_HEIGHT and 0 <= z < CHUNK_SIZE:
            return self.blocks[x, y, z]
        return 0  # Air


class World:
    """Manages all chunks and world logic"""
    def __init__(self):
        self.chunks = {}
        self.render_distance = 2
        self.last_player_chunk = None
    
    def get_chunk(self, x, z):
        """Get or create chunk at position"""
        key = (x, z)
        if key not in self.chunks:
            self.chunks[key] = Chunk(x, z)
            self.chunks[key].generate()
        return self.chunks[key]
    
    def get_block(self, x, y, z):
        """Get block type at world position"""
        chunk_x = int(x) // CHUNK_SIZE
        chunk_z = int(z) // CHUNK_SIZE
        block_x = int(x) % CHUNK_SIZE
        block_z = int(z) % CHUNK_SIZE
        
        chunk = self.get_chunk(chunk_x, chunk_z)
        return chunk.get_block(block_x, int(y), block_z)
    
    def set_block(self, x, y, z, block_type):
        """Set block at world position"""
        chunk_x = int(x) // CHUNK_SIZE
        chunk_z = int(z) // CHUNK_SIZE
        block_x = int(x) % CHUNK_SIZE
        block_z = int(z) % CHUNK_SIZE
        
        chunk = self.get_chunk(chunk_x, chunk_z)
        chunk.set_block(block_x, int(y), block_z, block_type)
    
    def update(self, dt):
        """Update world logic"""
        pass  # Placeholder for future water/lava flow, etc.
    
    def get_visible_chunks(self, player_pos):
        """Get chunks that should be rendered"""
        chunk_x = int(player_pos[0]) // CHUNK_SIZE
        chunk_z = int(player_pos[2]) // CHUNK_SIZE
        
        visible = []
        for dx in range(-self.render_distance, self.render_distance + 1):
            for dz in range(-self.render_distance, self.render_distance + 1):
                cx = chunk_x + dx
                cz = chunk_z + dz
                visible.append(self.get_chunk(cx, cz))
        
        return visible
    
    def is_solid(self, x, y, z):
        """Check if a block is solid (for collision)"""
        if y < 0 or y >= WORLD_HEIGHT:
            return False
        block_type = self.get_block(x, y, z)
        return block_type > 0 and block_type not in [9, 10]  # Not air, water, or lava
