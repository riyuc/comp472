import math
import copy
import time
import argparse


class MiniChess:
    def __init__(self, ai_depth=3, play_mode="H-H", use_alpha_beta=True, max_time=10, max_turns=100, heuristic="default"):
        self.current_game_state = self.init_board()
        self.ai_depth = ai_depth
        self.play_mode = play_mode  # "H-H", "H-AI", "AI-H", "AI-AI"
        self.use_alpha_beta = use_alpha_beta  # True for alpha-beta, False for regular minimax
        self.max_time = max_time
        self.max_turns = max_turns
        self.heuristic = heuristic

    """
    Initialize the board

    Args:
        - None
    Returns:
        - state: A dictionary representing the state of the game
    """
    def init_board(self):
        state = {
            "board":
                [
                    ['bK', 'bQ', 'bB', 'bN', '.'],
                    ['.', '.', 'bp', 'bp', '.'],
                    ['.', '.', '.', '.', '.'],
                    ['.', 'wp', 'wp', '.', '.'],
                    ['.', 'wN', 'wB', 'wQ', 'wK']
                ],
            "turn": 'white',
        }
        return state

    """
    Prints the board
    Args:
        - game_state: Dictionary representing the current game state
    Returns:
        - None
    """
    def display_board(self, game_state):
        print()
        for i, row in enumerate(game_state["board"], start=1):
            print(str(6-i) + "  " + ' '.join(piece.rjust(3) for piece in row))
        print()
        print("     A   B   C   D   E")
        print()

    """
    Check if the move is valid
    Args:
        - game_state:   dictionary | Dictionary representing the current game
          state
        - move          tuple | the move which we check the validity of
            ((start_row, start_col),(end_row, end_col))
    Returns:
        - boolean representing the validity of the move
    """
    def is_valid_move(self, game_state, move):
        valid_moves_list = self.valid_moves(game_state)
        return move in valid_moves_list

    """
    Returns a list of valid moves

    Args:
        - game_state:   dictionary | Dictionary representing
          the current game state
    Returns:
        - valid moves:   list | A list of nested tuples corresponding to
          valid moves [
            ((start_row, start_col),(end_row, end_col)),
            ((start_row, start_col),(end_row, end_col))
          ]
    """
    def valid_moves(self, game_state):
        # Return a list of all the valid moves.
        # Implement basic move validation
        # Check for out-of-bounds, correct turn, move legality, etc
        valid_moves_list = []
        board = game_state["board"]
        current_player = game_state["turn"]
        player_prefix = "w" if current_player == "white" else "b"
        for row in range(5):
            for col in range(5):
                piece = board[row][col]
                if piece.startswith(player_prefix):
                    piece_type = piece[1]
                    if piece_type == "p":
                        if player_prefix == "w":
                            if row > 0 and board[row-1][col] == ".":
                                valid_moves_list.append(
                                    ((row, col), (row-1, col))
                                )
                            if (
                                row > 0 and col > 0 and
                                board[row-1][col-1].startswith("b")
                            ):
                                valid_moves_list.append(
                                    ((row, col), (row-1, col-1))
                                )
                            if (
                                row > 0 and col < 4 and
                                board[row-1][col+1].startswith("b")
                            ):
                                valid_moves_list.append(
                                    ((row, col), (row-1, col+1))
                                )
                        else:
                            if row < 4 and board[row+1][col] == ".":
                                valid_moves_list.append(
                                    ((row, col), (row+1, col))
                                )
                            if (
                                row < 4 and col > 0 and
                                board[row+1][col-1].startswith("w")
                            ):
                                valid_moves_list.append(
                                    ((row, col), (row+1, col-1))
                                )
                            if (
                                    row < 4 and col < 4 and
                                    board[row+1][col+1].startswith("w")
                            ):
                                valid_moves_list.append(
                                    ((row, col), (row+1, col+1))
                                )
                    elif piece_type == "N":
                        knight_moves = [
                            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
                            (1, -2), (1, 2), (2, -1), (2, 1)
                        ]
                        for dr, dc in knight_moves:
                            new_row, new_col = row + dr, col + dc
                            if 0 <= new_row < 5 and 0 <= new_col < 5:
                                target = board[new_row][new_col]
                                if (
                                    target == "." or
                                    target.startswith(
                                        "b" if player_prefix == "w" else "w"
                                    )
                                ):
                                    valid_moves_list.append(
                                        ((row, col), (new_row, new_col))
                                    )
                    elif piece_type == "K":
                        king_moves = [
                            (-1, -1), (-1, 0), (-1, 1), (0, -1),
                            (0, 1), (1, -1), (1, 0), (1, 1)
                        ]
                        for dr, dc in king_moves:
                            new_row, new_col = row + dr, col + dc
                            if 0 <= new_row < 5 and 0 <= new_col < 5:
                                target = board[new_row][new_col]
                                if (
                                    target == "." or
                                    target.startswith(
                                        "b" if player_prefix == "w" else "w"
                                    )
                                ):
                                    valid_moves_list.append(
                                        ((row, col), (new_row, new_col))
                                    )
                    elif piece_type in ["B", "Q"]:
                        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
                        for dr, dc in directions:
                            for dist in range(1, 5):
                                new_row, new_col = row + dr * dist, col + dc * dist
                                if not (0 <= new_row < 5 and 0 <= new_col < 5):
                                    break
                                target = board[new_row][new_col]
                                if target == ".":
                                    valid_moves_list.append(
                                        ((row, col), (new_row, new_col))
                                    )
                                elif target.startswith("b" if player_prefix == "w" else "w"):
                                    valid_moves_list.append(
                                        ((row, col), (new_row, new_col))
                                    )
                                    break
                                else:
                                    break
                    if piece_type in ["Q", "R"]:
                        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                        for dr, dc in directions:
                            for dist in range(1, 5):
                                new_row, new_col = row + dr * dist, col + dc * dist
                                if not (0 <= new_row < 5 and 0 <= new_col < 5):
                                    break
                                target = board[new_row][new_col]
                                if target == ".":
                                    valid_moves_list.append(
                                        ((row, col), (new_row, new_col)))
                                elif target.startswith("b" if player_prefix == "w" else "w"):
                                    valid_moves_list.append(
                                        ((row, col), (new_row, new_col)))
                                    break
                                else:
                                    break
        return valid_moves_list

    """
    Modify to board to make a move

    Args:
        - game_state:   dictionary | Dictionary representing the
          current game state
        - move          tuple | the move to perform
          ((start_row, start_col),(end_row, end_col))
    Returns:
        - game_state:   dictionary | Dictionary representing the
          modified game state
    """
    def make_move(self, game_state, move):
        start, end = move[0], move[1]
        start_row, start_col = start
        end_row, end_col = end
        piece = game_state["board"][start_row][start_col]
        if piece == "wp" and end_row == 0:
            piece = "wQ"
        elif piece == "bp" and end_row == 4:
            piece = "bQ"
        game_state["board"][start_row][start_col] = '.'
        game_state["board"][end_row][end_col] = piece
        game_state["turn"] = "black" if game_state["turn"] == "white" else "white"
        return game_state

    """
    Parse the input string and modify it into board coordinates

    Args:
        - move: string representing a move "B2 B3"
    Returns:
        - (start, end)  tuple | the move to perform
          ((start_row, start_col),(end_row, end_col))
    """
    def parse_input(self, move):
        try:
            start, end = move.split()
            start = (5-int(start[1]), ord(start[0].upper()) - ord('A'))
            end = (5-int(end[1]), ord(end[0].upper()) - ord('A'))
            return (start, end)
        except:
            return None

    """
    Check if a player has won by capturing the opponent's king
    
    Args:
        - game_state: Dictionary representing the current game state
    Returns:
        - String: "white", "black", or None (if no winner)
    """
    def check_winner(self, game_state):
        board = game_state["board"]
        white_king_exists = any("wK" in row for row in board)
        black_king_exists = any("bK" in row for row in board)
        
        if not white_king_exists:
            return "black"
        if not black_king_exists:
            return "white"
        return None

    """
    Format a board to string for display
    
    Args:
        - board: 2D array representing the chess board
    Returns:
        - String: Formatted board representation
    """
    def format_board(self, board):
        result = ""
        for i, row in enumerate(board, start=1):
            result += f"{6-i}  {' '.join(piece.rjust(3) for piece in row)}\n"
        result += "\n     A   B   C   D   E\n"
        return result

    """
    Game loop

    Args:
        - None
    Returns:
        - None
    """
    def play(self):
        print(f"Welcome to Mini Chess! Play mode: {self.play_mode}")
        print("Enter moves as 'B2 B3'. Type 'exit' to quit.")
        
        turn_counter = 0
        last_capture_turn = 0
        
        white_ai = None
        black_ai = None
        
        white_heuristic_name = "e0"
        black_heuristic_name = "e0"
        
        if self.play_mode in ["H-AI", "AI-AI"]:
            # For H-AI mode, use default heuristic for black
            if self.play_mode == "H-AI":
                black_ai = AIPlayer(self, self.ai_depth, "black", self.use_alpha_beta, self.max_time, "default")
                black_heuristic_name = "e0"
            # For AI-AI mode, use custom heuristic for black
            else:
                black_ai = AIPlayer(self, self.ai_depth, "black", self.use_alpha_beta, self.max_time, "custom2")
                black_heuristic_name = "e2"
                
        if self.play_mode in ["AI-H", "AI-AI"]:
            # For AI-H mode, use default heuristic for white
            if self.play_mode == "AI-H":
                white_ai = AIPlayer(self, self.ai_depth, "white", self.use_alpha_beta, self.max_time, "default")
                white_heuristic_name = "e0"
            # For AI-AI mode, use custom heuristic for white
            else:
                white_ai = AIPlayer(self, self.ai_depth, "white", self.use_alpha_beta, self.max_time, "custom1")
                white_heuristic_name = "e1"
        
        alpha_beta_str = "true" if self.use_alpha_beta else "false"
        file_name = f"gameTrace-{alpha_beta_str}-{self.max_time}-{self.max_turns}.txt"
        
        # Track cumulative statistics for AI players
        white_stats = {
            "total_nodes": 0,
            "nodes_by_depth": {},
            "moves_made": 0,
            "total_branches": 0
        }
        
        black_stats = {
            "total_nodes": 0,
            "nodes_by_depth": {},
            "moves_made": 0,
            "total_branches": 0
        }
        
        with open(file_name, "w") as f:
            f.write("1. Game parameters:\n")
            f.write(f"a) Timeout: {self.max_time} seconds\n")
            f.write(f"b) Maximum turns: {self.max_turns}\n")
            f.write(f"c) Play mode: ")
            
            if self.play_mode == "H-H":
                f.write("Player 1 = H & Player 2 = H\n")
            elif self.play_mode == "H-AI":
                f.write("Player 1 = H & Player 2 = AI\n")
            elif self.play_mode == "AI-H":
                f.write("Player 1 = AI & Player 2 = H\n")
            else:  # AI-AI
                f.write("Player 1 = AI & Player 2 = AI\n")
            
            if white_ai:
                f.write(f"d) Player 1 (white) uses {'alpha-beta' if self.use_alpha_beta else 'minimax'}\n")
                f.write(f"e) Player 1 (white) heuristic: {white_heuristic_name}\n")
            
            if black_ai:
                f.write(f"d) Player 2 (black) uses {'alpha-beta' if self.use_alpha_beta else 'minimax'}\n")
                f.write(f"e) Player 2 (black) heuristic: {black_heuristic_name}\n")
            
            f.write("\n2. Initial configuration of the board:\n")
            f.write(self.format_board(self.current_game_state["board"]))
            f.write("\n")
            
        while True:
            self.display_board(self.current_game_state)
            
            if turn_counter >= self.max_turns * 2:  # *2 because each player's move counts as 1 turn
                print(f"The game is a draw because the maximum number of turns ({self.max_turns}) has been reached.")
                with open(file_name, "a") as f:
                    f.write(f"\n4. The game ended in a draw after {turn_counter // 2} turns (maximum turns reached)\n")
                break
            
            winner = self.check_winner(self.current_game_state)
            if winner:
                print(f"{winner.capitalize()} wins by capturing the {('white' if winner == 'black' else 'black')} king")
                with open(file_name, "a") as f:
                    f.write(f"\n4. {winner.capitalize()} won in {turn_counter // 2} turns\n")
                break
                
            if turn_counter - last_capture_turn >= 10 * 2:
                print("The game is a draw because 10 turns have passed without a capture.")
                with open(file_name, "a") as f:
                    f.write(f"\n4. The game ended in a draw after {turn_counter // 2} turns (10 turns without capture)\n")
                break
                
            current_turn = self.current_game_state["turn"]
            
            move = None
            is_ai_move = False
            ai_stats = {"nodes": 0, "time": 0, "heuristic": "", "board_score": 0, "search_score": 0, "nodes_by_depth": {}}
            
            if (current_turn == "white" and white_ai) or (current_turn == "black" and black_ai):
                ai = white_ai if current_turn == "white" else black_ai
                heuristic_name = white_heuristic_name if current_turn == "white" else black_heuristic_name
                stats = white_stats if current_turn == "white" else black_stats
                
                print(f"{current_turn.capitalize()} (AI using {heuristic_name} heuristic) is thinking...")
                
                start_time = time.time()
                move, nodes_explored, board_score, search_score, nodes_by_depth = ai.get_best_move_with_stats(self.current_game_state)
                end_time = time.time()
                elapsed_time = end_time - start_time
                
                # Update cumulative statistics
                stats["total_nodes"] += nodes_explored
                stats["moves_made"] += 1
                
                # Calculate branches explored at each depth
                total_branches = 0
                for depth, count in nodes_by_depth.items():
                    if depth in stats["nodes_by_depth"]:
                        stats["nodes_by_depth"][depth] += count
                    else:
                        stats["nodes_by_depth"][depth] = count
                        
                    # For branching factor, count all non-root nodes
                    if depth > 0:
                        total_branches += count
                
                stats["total_branches"] += total_branches
                
                start_coords = f"{chr(ord('A') + move[0][1])}{5 - move[0][0]}"
                end_coords = f"{chr(ord('A') + move[1][1])}{5 - move[1][0]}"
                print(f"AI move: {start_coords} {end_coords} (explored {nodes_explored} nodes in {elapsed_time:.2f} seconds)")
                
                is_ai_move = True
                ai_stats = {
                    "nodes": nodes_explored, 
                    "time": elapsed_time, 
                    "heuristic": heuristic_name,
                    "board_score": board_score,
                    "search_score": search_score,
                    "nodes_by_depth": nodes_by_depth,
                    "stats": stats
                }
                
            else:
                # Human player's turn
                move_input = input(f"{current_turn.capitalize()} to move: ")
                if move_input.lower() == 'exit':
                    print("Game exited.")
                    break
                    
                move = self.parse_input(move_input)
                if not move or not self.is_valid_move(self.current_game_state, move):
                    print("Invalid move. Try again.")
                    continue
            
            start, end = move
            end_row, end_col = end
            target_square = self.current_game_state["board"][end_row][end_col]
            if target_square != ".":
                is_capture = True
                last_capture_turn = turn_counter
            else:
                is_capture = False
                
            old_state = copy.deepcopy(self.current_game_state)
            self.current_game_state = self.make_move(self.current_game_state, move)
            
            with open(file_name, "a") as f:
                start_coords = f"{chr(ord('A') + move[0][1])}{5 - move[0][0]}"
                end_coords = f"{chr(ord('A') + move[1][1])}{5 - move[1][0]}"
                
                f.write(f"3. {old_state['turn']} turn #{turn_counter // 2 + 1}\n")
                f.write(f"3.1. Information about the action:\n")
                f.write(f"a) Player: {old_state['turn']}\n")
                f.write(f"b) Turn #{turn_counter // 2 + 1}\n")
                f.write(f"c) Move from {start_coords} to {end_coords}\n")
                
                if is_ai_move:
                    f.write(f"d) Time for this action: {ai_stats['time']:.2f} sec\n")
                    f.write(f"e) Heuristic score: {ai_stats['board_score']}\n")
                    f.write(f"f) {'Alpha-beta' if self.use_alpha_beta else 'Minimax'} search score: {ai_stats['search_score']}\n")
                
                f.write(f"g) New board configuration:\n")
                f.write(self.format_board(self.current_game_state["board"]))
                
                # Add cumulative AI statistics
                if is_ai_move:
                    stats = ai_stats["stats"]
                    
                    f.write(f"3.2. Cumulative information about the game so far:\n")
                    
                    total_nodes_str = self.format_large_number(stats["total_nodes"])
                    f.write(f"a) Cumulative states explored: {total_nodes_str}\n")
                    
                    f.write(f"b) Cumulative states explored by depth: ")
                    depth_strs = []
                    for depth in sorted(stats["nodes_by_depth"].keys()):
                        count = stats["nodes_by_depth"][depth]
                        depth_strs.append(f"{depth}={self.format_large_number(count)}")
                    f.write(" ".join(depth_strs) + "\n")
                    
                    f.write(f"c) Cumulative % states explored by depth: ")
                    percentage_strs = []
                    for depth in sorted(stats["nodes_by_depth"].keys()):
                        count = stats["nodes_by_depth"][depth]
                        percentage = (count / stats["total_nodes"]) * 100
                        percentage_strs.append(f"{depth}={percentage:.1f}%")
                    f.write(" ".join(percentage_strs) + "\n")
                    
                    if stats["moves_made"] > 0:
                        avg_branching = stats["total_branches"] / stats["total_nodes"] if stats["total_nodes"] > 0 else 0
                        f.write(f"d) Average branching factor: {avg_branching:.1f}\n")
                    
                f.write("\n")
                
            turn_counter += 1

    def format_large_number(self, num):
        if num < 1000:
            return str(num)
        elif num < 1000000:
            return f"{num/1000:.1f}k".replace('.0k', 'k')
        elif num < 1000000000:
            return f"{num/1000000:.1f}M".replace('.0M', 'M')
        else:
            return f"{num/1000000000:.1f}B".replace('.0B', 'B')


class AIPlayer:
    def __init__(self, game, depth=3, player_color='black', use_alpha_beta=True, max_time=10, heuristic="default"):
        self.game = game
        self.max_depth = depth
        self.player_color = player_color
        self.nodes_explored = 0
        self.use_alpha_beta = use_alpha_beta
        self.max_time = max_time
        self.start_time = 0
        self.heuristic = heuristic
        self.nodes_by_depth = {}
        
    """
    Heuristic evaluation functions
    """
    def evaluate_board(self, game_state):
        if self.heuristic == "default":
            return self.default_heuristic(game_state)
        elif self.heuristic == "custom1":
            return self.custom_heuristic1(game_state)
        elif self.heuristic == "custom2":
            return self.custom_heuristic2(game_state)
        else:
            # Fallback to default
            return self.default_heuristic(game_state)
        

    def default_heuristic(self, game_state):
        # This is the specific heuristic mentioned in the assignment
        piece_values = {'K': 999, 'Q': 9, 'B': 3, 'N': 3, 'p': 1}
        board = game_state["board"]
        score = 0
        
        for row in range(5):
            for col in range(5):
                piece = board[row][col]
                if piece != '.':
                    value = piece_values.get(piece[1], 0)
                    if piece.startswith('w'):
                        score += value
                    else:
                        score -= value
        
        return score if self.player_color == "white" else -score
    
    """
    Custom heuristic 1 - Used by white AI in AI-AI mode
    More sophisticated heuristic that focuses on piece mobility and center control
    """
    def custom_heuristic1(self, game_state):
        piece_values = {'K': 200, 'Q': 9, 'B': 3, 'N': 3, 'p': 1}
        board = game_state["board"]
        score = 0
        
        for row in range(5):
            for col in range(5):
                piece = board[row][col]
                if piece != '.':
                    value = piece_values.get(piece[1], 0)
                    if piece.startswith('w'):
                        score += value
                    else:
                        score -= value
        
        # Position evaluation - pawns
        for row in range(5):
            for col in range(5):
                piece = board[row][col]
                if piece == 'wp':
                    score += (4 - row) * 0.2
                elif piece == 'bp':
                    score -= row * 0.2
        
        center_squares = [(1, 2), (2, 1), (2, 2), (2, 3), (3, 2)]
        for row, col in center_squares:
            piece = board[row][col]
            if piece.startswith('w'):
                score += 0.3
            elif piece.startswith('b'):
                score -= 0.3
        
        # Piece mobility evaluation
        for row in range(5):
            for col in range(5):
                piece = board[row][col]
                # Only calculate mobility for high-value pieces
                if piece in ['wQ', 'wB', 'wN', 'bQ', 'bB', 'bN']:
                    # Create a temporary game state with this piece's turn
                    temp_state = copy.deepcopy(game_state)
                    temp_state["turn"] = "white" if piece.startswith('w') else "black"
                    
                    # Count moves for this piece
                    moves = 0
                    for move in self.game.valid_moves(temp_state):
                        if move[0] == (row, col):
                            moves += 1
                    
                    # Add mobility score
                    if piece.startswith('w'):
                        score += moves * 0.05
                    else:
                        score -= moves * 0.05
        
        return score if self.player_color == "white" else -score
    
    """
    Custom heuristic 2 - Used by black AI in AI-AI mode
    A different approach that focuses on king safety and attacking opportunities
    """
    def custom_heuristic2(self, game_state):
        piece_values = {'K': 200, 'Q': 9, 'B': 3, 'N': 3, 'p': 1}
        board = game_state["board"]
        score = 0
        
        for row in range(5):
            for col in range(5):
                piece = board[row][col]
                if piece != '.':
                    value = piece_values.get(piece[1], 0)
                    if piece.startswith('w'):
                        score += value
                    else:
                        score -= value
        
        white_king_pos = None
        black_king_pos = None
        
        # Find king positions
        for row in range(5):
            for col in range(5):
                if board[row][col] == 'wK':
                    white_king_pos = (row, col)
                elif board[row][col] == 'bK':
                    black_king_pos = (row, col)
        
        # Evaluate king safety based on surrounding pieces and exposure
        if white_king_pos:
            row, col = white_king_pos
            defenders = 0
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    r, c = row + dr, col + dc
                    if 0 <= r < 5 and 0 <= c < 5:
                        if board[r][c].startswith('w'):
                            defenders += 1
                        elif board[r][c].startswith('b'):
                            # Enemy piece threatening the king
                            score -= 0.5
            
            score += defenders * 0.3
            
            # Penalty for exposed king
            if 1 <= row <= 3 and 1 <= col <= 3:
                score -= 0.4
        
        if black_king_pos:
            row, col = black_king_pos
            defenders = 0
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    r, c = row + dr, col + dc
                    if 0 <= r < 5 and 0 <= c < 5:
                        if board[r][c].startswith('b'):
                            defenders += 1
                        elif board[r][c].startswith('w'):
                            score += 0.5
            
            score -= defenders * 0.3
            
            # Penalty for exposed king
            if 1 <= row <= 3 and 1 <= col <= 3:
                score += 0.4
        
        # Attacking potential - evaluate control of opponent's territory
        white_control = 0
        black_control = 0
        
        for row in range(2):
            for col in range(5):
                piece = board[row][col]
                if piece.startswith('w'):
                    white_control += 1
        
        for row in range(3, 5):
            for col in range(5):
                piece = board[row][col]
                if piece.startswith('b'):
                    black_control += 1
        
        score += white_control * 0.2
        score -= black_control * 0.2
        
        return score if self.player_color == "white" else -score
    
    def is_time_up(self):
        return time.time() - self.start_time >= self.max_time
    
    def minimax(self, game_state, depth, maximizing_player):
        self.nodes_explored += 1
        
        # Track nodes by depth
        if depth in self.nodes_by_depth:
            self.nodes_by_depth[depth] += 1
        else:
            self.nodes_by_depth[depth] = 1
        
        if self.is_time_up():
            return self.evaluate_board(game_state)
        
        winner = self.game.check_winner(game_state)
        if winner == "white":
            return 1000 if self.player_color == "white" else -1000
        if winner == "black":
            return -1000 if self.player_color == "white" else 1000
            
        if depth == 0:
            return self.evaluate_board(game_state)
            
        valid_moves = self.game.valid_moves(game_state)
        if not valid_moves:
            return 0  # Draw
            
        if maximizing_player:
            max_eval = float('-inf')
            for move in valid_moves:
                new_state = copy.deepcopy(game_state)
                new_state = self.game.make_move(new_state, move)
                eval = self.minimax(new_state, depth-1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                new_state = copy.deepcopy(game_state)
                new_state = self.game.make_move(new_state, move)
                eval = self.minimax(new_state, depth-1, True)
                min_eval = min(min_eval, eval)
            return min_eval
    
    def alpha_beta(self, game_state, depth, alpha, beta, maximizing_player):
        self.nodes_explored += 1
        
        if depth in self.nodes_by_depth:
            self.nodes_by_depth[depth] += 1
        else:
            self.nodes_by_depth[depth] = 1
        
        if self.is_time_up():
            return self.evaluate_board(game_state)
        
        winner = self.game.check_winner(game_state)
        if winner == "white":
            return 1000 if self.player_color == "white" else -1000
        if winner == "black":
            return -1000 if self.player_color == "white" else 1000
            
        if depth == 0:
            return self.evaluate_board(game_state)
            
        valid_moves = self.game.valid_moves(game_state)
        if not valid_moves:
            return 0  # Draw
            
        # Order moves to improve alpha-beta efficiency
        ordered_moves = self.order_moves(game_state, valid_moves)
            
        if maximizing_player:
            max_eval = float('-inf')
            for move in ordered_moves:
                new_state = copy.deepcopy(game_state)
                new_state = self.game.make_move(new_state, move)
                eval = self.alpha_beta(new_state, depth-1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in ordered_moves:
                new_state = copy.deepcopy(game_state)
                new_state = self.game.make_move(new_state, move)
                eval = self.alpha_beta(new_state, depth-1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
    

    def order_moves(self, game_state, moves):
        # Simple move ordering: captures first, then center moves
        captures = []
        center_moves = []
        other_moves = []
        
        for move in moves:
            end_row, end_col = move[1]
            if game_state["board"][end_row][end_col] != ".":
                captures.append(move)
            elif 1 <= end_row <= 3 and 1 <= end_col <= 3:
                center_moves.append(move)
            else:
                other_moves.append(move)
                
        return captures + center_moves + other_moves
    
    def get_best_move_with_stats(self, game_state):
        self.nodes_explored = 0
        self.nodes_by_depth = {}
        self.start_time = time.time()
        
        best_value = float('-inf') if game_state["turn"] == "white" else float('inf')
        best_move = None
        search_score = 0
        valid_moves = self.game.valid_moves(game_state)
        
        if len(valid_moves) == 1:
            move = valid_moves[0]
            new_state = copy.deepcopy(game_state)
            new_state = self.game.make_move(new_state, move)
            board_score = self.evaluate_board(new_state)
            return move, 1, board_score, board_score, {0: 1}
        
        ordered_moves = self.order_moves(game_state, valid_moves)
        
        is_maximizing = game_state["turn"] == "white"
        
        if self.use_alpha_beta:
            alpha = float('-inf')
            beta = float('inf')
            
            for move in ordered_moves:
                if self.is_time_up():
                    if best_move is None and ordered_moves:
                        best_move = ordered_moves[0]
                        new_state = copy.deepcopy(game_state)
                        new_state = self.game.make_move(new_state, best_move)
                        board_score = self.evaluate_board(new_state)
                        return best_move, self.nodes_explored, board_score, 0, self.nodes_by_depth
                    break
                    
                new_state = copy.deepcopy(game_state)
                new_state = self.game.make_move(new_state, move)
                
                value = self.alpha_beta(new_state, self.max_depth-1, alpha, beta, not is_maximizing)
                
                if is_maximizing and value > best_value:
                    best_value = value
                    best_move = move
                    search_score = value
                    alpha = max(alpha, best_value)
                elif not is_maximizing and value < best_value:
                    best_value = value
                    best_move = move
                    search_score = value
                    beta = min(beta, best_value)
        else:
            for move in ordered_moves:
                if self.is_time_up():
                    if best_move is None and ordered_moves:
                        best_move = ordered_moves[0]
                        new_state = copy.deepcopy(game_state)
                        new_state = self.game.make_move(new_state, best_move)
                        board_score = self.evaluate_board(new_state)
                        return best_move, self.nodes_explored, board_score, 0, self.nodes_by_depth
                    break
                    
                new_state = copy.deepcopy(game_state)
                new_state = self.game.make_move(new_state, move)
                
                value = self.minimax(new_state, self.max_depth-1, not is_maximizing)
                
                if is_maximizing and value > best_value:
                    best_value = value
                    best_move = move
                    search_score = value
                elif not is_maximizing and value < best_value:
                    best_value = value
                    best_move = move
                    search_score = value
        
        if best_move is None and valid_moves:
            best_move = valid_moves[0]
            new_state = copy.deepcopy(game_state)
            new_state = self.game.make_move(new_state, best_move)
            board_score = self.evaluate_board(new_state)
            return best_move, self.nodes_explored, board_score, 0, self.nodes_by_depth
        
        result_state = copy.deepcopy(game_state)
        result_state = self.game.make_move(result_state, best_move)
        board_score = self.evaluate_board(result_state)
        
        return best_move, self.nodes_explored, board_score, search_score, self.nodes_by_depth
    
    def get_best_move(self, game_state):
        move, nodes, _, _, _ = self.get_best_move_with_stats(game_state)
        return move, nodes


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Mini Chess Game')
    parser.add_argument('--mode', type=str, default='H-H', choices=['H-H', 'H-AI', 'AI-H', 'AI-AI'],
                      help='Play mode: Human-Human, Human-AI, AI-Human, or AI-AI')
    parser.add_argument('--depth', type=int, default=3,
                      help='AI search depth (default: 3)')
    parser.add_argument('--alpha-beta', type=bool, default=True,
                      help='Use alpha-beta pruning (TRUE) or regular minimax (FALSE)')
    parser.add_argument('--max-time', type=int, default=10,
                      help='Maximum allowed time in seconds for AI to make a move (default: 10)')
    parser.add_argument('--max-turns', type=int, default=100,
                      help='Maximum number of turns before the game is declared a draw (default: 100)')
    
    args = parser.parse_args()
    
    game = MiniChess(
        ai_depth=args.depth,
        play_mode=args.mode,
        use_alpha_beta=args.alpha_beta,
        max_time=args.max_time,
        max_turns=args.max_turns
    )
    game.play()