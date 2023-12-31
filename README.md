
 # Pacman Game

## Overview

This repository contains a simple Pacman game implemented in Python using the Tkinter library for the graphical user interface. The game environment is represented by a 2D grid, and the player controls Pacman to collect food while avoiding ghosts.

## Features

- **Pacman and Ghosts:** The game includes Pacman and ghosts as characters on the grid.
- **Score System:** Pacman scores points by collecting food, and the score is displayed during the game.
- **Game Over Conditions:** The game ends when Pacman collects all the food or encounters ghosts. The result (win or loss) is displayed at the end of the game.


## Implementation Details

- **Game Class:** The core game logic is implemented in the `Game` class, handling initialization, positions of Pacman and ghosts, and other game-related functionality.
- **AI (Minimax Algorithm):** The ghosts' movements are controlled by a simple AI using the minimax algorithm to make decisions based on the current game state.
- **Tkinter GUI:** The game utilizes the Tkinter library for creating the graphical user interface, including the game grid and score display.

## Dependencies

- NumPy
- Tkinter
- PIL (Pillow)

   Install the dependencies using the following:

   ```bash
   pip install numpy pillow



## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve the game.



