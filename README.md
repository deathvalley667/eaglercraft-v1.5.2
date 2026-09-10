# Eaglercraft v1.5.2

A Python implementation of a Minecraft-inspired game engine. This project recreates the core gameplay mechanics of Minecraft in a playable Python application.

## Features

- **3D World Generation**: Procedurally generated terrain with multiple block types
- **Player Movement**: WASD movement with smooth camera control
- **Physics System**: Gravity, jumping, and collision detection
- **Block System**: Multiple block types (stone, grass, dirt, water, lava, sand, etc.)
- **Rendering**: Perspective projection rendering of 3D blocks
- **Game Loop**: 60 FPS game engine with proper frame timing

## Installation

1. Install Python 3.8 or higher
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Game

```bash
python main.py
```

## Controls

- **W/A/S/D** - Move forward/left/backward/right
- **Space** - Jump
- **Mouse** - Look around (move mouse to rotate camera)
- **ESC** - Quit game
- **P** - Pause game
- **F** - Toggle flying mode

## Game Features

### World
- Infinite procedurally generated terrain
- Multiple biome-like regions with varying terrain heights
- Chunk-based world management for scalability

### Player
- First-person camera view
- Smooth movement with acceleration/deceleration
- Jump mechanics with gravity simulation
- Flying mode for creative play
- Health and hunger systems (placeholder)

### Blocks
The game includes 10 different block types:
1. **Air** (transparent, no collision)
2. **Stone** - Gray blocks found deep underground
3. **Grass** - Green blocks at terrain surface
4. **Dirt** - Brown blocks underground
5. **Cobblestone** - Darker gray blocks
6. **Oak Log** - Brown wooden blocks
7. **Oak Leaves** - Green foliage
8. **Sand** - Light yellow blocks in deserts
9. **Gravel** - Light gray blocks
10. **Water** - Blue liquid (decorative)
11. **Lava** - Red liquid (decorative)

## Architecture

```
eaglercraft-v1.5.2/
├── main.py              # Game entry point
├── config.py            # Game configuration and constants
├── requirements.txt     # Python dependencies
├── README.md            # This file
└── game/
    ├── engine.py        # Main game loop and engine
    ├── world.py         # World generation and chunk management
    ├── player.py        # Player entity and movement
    ├── renderer.py      # Rendering system
    └── input_handler.py # Input management
```

## Technical Details

### Rendering
The renderer uses a custom perspective projection system to convert 3D world coordinates to 2D screen coordinates. Blocks are rendered with depth-based shading for visual depth.

### Physics
The physics engine handles:
- Gravity and falling
- Collision detection using AABB (Axis-Aligned Bounding Box)
- Jump mechanics
- Velocity-based movement

### World Generation
Terrain is generated using layered Perlin-noise-like algorithms to create natural-looking hills and valleys. The world is divided into 16×256×16 chunks for efficient management.

## Future Enhancements

- [ ] Block breaking and placing
- [ ] Inventory system
- [ ] Crafting system
- [ ] Multiplayer networking
- [ ] Advanced lighting and shadows
- [ ] Texture mapping
- [ ] Mob entities
- [ ] Save/load world data
- [ ] Sound effects and music
- [ ] Advanced terrain generation biomes

## License

This project is created for educational purposes as a recreation of Minecraft's core gameplay mechanics.

## Credits

Inspired by Minecraft and the Eaglercraft project.
