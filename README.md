# Mini Chess Game - COMP 472

A small scale chess variant built in Python, featuring both human vs. human play and human vs. AI (or AI vs. AI) matchups.

## Features
- Play modes:  
  • H-H   (Human vs. Human)  
  • H-AI  (Human vs. AI)  
  • AI-H  (AI vs. Human)  
  • AI-AI (AI vs. AI)  
- AI search depth (default 3)  
- Optional alpha-beta pruning (default True)  
- Maximum thinking time per move (default 10 seconds)  
- Maximum turns before automatic draw (default 100)

## Usage
1. Install Python 3 if not already installed.  
2. In a terminal, navigate to the project folder:  
   ```bash
   cd comp472
   ```
3. Run the game with default parameters:  
   ```bash
   python game2.py
   ```
4. Pass command-line arguments if needed:  
   ```bash
   python game2.py \
     --mode AI-AI \
     --depth 4 \
     --alpha-beta True \
     --max-time 15 \
     --max-turns 80
   ```

## Code Structure
- **MiniChess**: Initializes and manages the board state, input parsing, and main game loop.  
- **AIPlayer**: Implements minimax or alpha‐beta pruning, plus different heuristic evaluations.

## Acknowledgments
This project was created as part of COMP 472 coursework, analyzing basic chess heuristics and search algorithms. Feel free to modify or expand the code to try out new heuristics or debugging techniques.
