import chess
import torch

# Function to convert a move (in algebraic notation) to input tensor
def move_to_input(move_str):
    move = chess.Move.from_uci(move_str)  # Convert move string to move object
    input_tensor = [0] * 64  # Initialize a list of 64 zeros

    # Convert the move to a square index
    from_square = move.from_square
    to_square = move.to_square

    # Set the corresponding indices to 1
    input_tensor[from_square] = 1.0
    input_tensor[to_square] = 1.0

    return input_tensor

# Function to convert a result to target tensor
def result_to_target(result):
    if result == '1-0':
        return [1.0]  # White wins
    elif result == '0-1':
        return [-1.0]  # Black wins
    else:
        return [0.0]  # Draw
    
