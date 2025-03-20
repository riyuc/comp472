# import math
import copy
# import time
# import argparse


class MiniChess:
    def __init__(self):
        self.current_game_state = self.init_board()

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
        # Check if move is in list of valid moves
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
    Game loop

    Args:
        - None
    Returns:
        - None
    """

    def play(self):
        print("Welcome to Mini Chess! Enter moves as 'B2 B3'. Type 'exit' to quit.")
        turn_counter = 0
        last_capture_turn = 0
        turn_draw_counter = 0
        with open("gameTrace-false-0-0.txt", "w") as f:
            f.write("Game parameters:\n")
            f.write("Play mode: H-H\n")
            f.write("Initial board configuration:\n")
            for i, row in enumerate(self.current_game_state["board"], start=1):
                row_number = 6 - i
                formatted_row = ' '.join(piece.rjust(3) for piece in row)
                f.write(f"{row_number}  {formatted_row}\n")
            f.write("\n     A   B   C   D   E\n\n")
        while True:
            self.display_board(self.current_game_state)
            board = self.current_game_state["board"]
            white_king_exists = any("wK" in row for row in board)
            black_king_exists = any("bK" in row for row in board)
            if not white_king_exists:
                print("Black wins by capturing the white king")
                with open("gameTrace-false-0-0.txt", "a") as f:
                    f.write("Black wins by capturing the white king\n")
                break
            if not black_king_exists:
                print("White wins by capturing the black king")
                with open("gameTrace-false-0-0.txt", "a") as f:
                    f.write("White wins by capturing the black king\n")
                break
            if turn_counter - last_capture_turn >= 10 * 2:
                print(
                    "The game is a draw because 10 turns have passed without a capture.")
                with open("gameTrace-false-0-0.txt", "a") as f:
                    f.write(
                        "The game is a draw because 10 turns have passed without a capture.\n")
                break
            move_input = input(
                f"{self.current_game_state['turn'].capitalize()} to move: ")
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
            else:
                is_capture = False
            old_state = copy.deepcopy(self.current_game_state)
            self.current_game_state = self.make_move(
                self.current_game_state, move)
            if is_capture:
                last_capture_turn = turn_counter
            with open("gameTrace-false-0-0.txt", "a") as f:
                start_coords = f"{chr(ord('A') + move[0][1])}{5 - move[0][0]}"
                end_coords = f"{chr(ord('A') + move[1][1])}{5 - move[1][0]}"
                f.write(f"{old_state['turn']} turn #{turn_counter // 2 + 1}\n")
                f.write(f"move from {start_coords} to {end_coords}\n\n")
                for i, row in enumerate(self.current_game_state["board"], start=1):
                    f.write(str(6-i) + "  " + ' '.join(piece.rjust(3)
                            for piece in row) + "\n")
                f.write("\n     A   B   C   D   E\n\n")
            turn_counter += 1


if __name__ == "__main__":
    game = MiniChess()
    game.play()
