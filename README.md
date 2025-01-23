# Flappy Bird Game Using Pygame and NEAT

## Overview
A Flappy Bird-inspired game built with Python's `pygame`. The bird moves through pipes while gravity and user input control its motion. NEAT AI integration will allow the game to train an AI to play.

## Current Features

### (1/22/2025)
- **Game Window**: 600x800 pixels.
- **Graphics**: Animated bird (3 images), pipes, base, and background.
- **Bird Class**: Handles position, tilt, velocity, jumping, and movement (in progress).

### (1/23/2025)
- **Updated Game Window**: Dimensions changed to 500x800 pixels.
- **Bird Movement**: Completed bird movement logic with realistic physics (arc motion).
- **Collision Masks**: Added detailed collision detection using pixel-perfect masks for bird and pipes.
- **Pipe Class**:
  - Randomized pipe heights for dynamic gameplay.
  - Pipe movement logic and collision handling implemented.
- **Base Class**: Added ground movement simulation to enhance visual realism.
- **Drawing Functions**: Background, bird, pipes, and base are dynamically drawn for every frame.

## Next Steps
- Add scoring system and dynamic pipe generation.
- Implement NEAT AI to train autonomous bird gameplay.
- Enhance UI elements (score display, start/restart screens, etc.).

## How to Run
1. Install `pygame`: `pip install pygame`.
2. Place images in an `imgs` folder.
3. Run the script: `python flappy_bird.py`.