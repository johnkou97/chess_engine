import chess
import random
import chess.svg
import subprocess
import os
import time
from stockfish import Stockfish
import torch


class ChessEnvironment:
    def __init__(self, stockfish_depth=10):
        self.board = chess.Board()
        self.svg_frames = []
        self.engine = Stockfish("stockfish/stockfish-ubuntu-x86-64")
        self.depth = stockfish_depth
        self.engine.set_depth(self.depth)
        self.done = False

    def reset(self):
        self.board.reset()
        self.svg_frames = []
        self.done = False
        return self.board.fen()

    def step(self, move):
        self.board.push(move)

        if self.board.is_game_over():
            result = self.board.result()
            if result == "1-0":
                reward = 1.0  # White wins
            elif result == "0-1":
                reward = -1.0  # Black wins
            else:
                reward = 0.0  # Draw
            self.done = True
        else:
            reward = 0.0
            self.done = False

        return self.board.fen(), reward, self.done

    def legal_moves(self):
        return list(self.board.legal_moves)

    def random_move(self):
        move = random.choice(list(self.board.legal_moves))
        return move

    def engine_move(self):
        self.engine.set_fen_position(self.board.fen())
        best_move = self.engine.get_best_move()
        move = chess.Move.from_uci(best_move)
        return move


    def render(self):
        print(self.board)

    def save_game_frames(self, directory):
        svg = chess.svg.board(board=self.board)
        self.svg_frames.append(svg)

        if self.done:
            # if folder exists, delete the contents
            if os.path.exists(directory):
                for file in os.listdir(directory):
                    os.remove(os.path.join(directory, file))
            else:    
                os.makedirs(directory)

            # Save each SVG frame to a separate file
            for i, svg in enumerate(self.svg_frames):
                frame_path = os.path.join(directory, f'frame_{i}.svg')
                with open(frame_path, 'w') as f:
                    f.write(svg)

    def create_animation(self, frames_directory, output_filename, delay=100):
        # Convert SVG frames to PNG
        subprocess.run(['convert', '-delay', str(delay), f'{frames_directory}/*.svg', output_filename])
    
    def get_fen_tensor(self):
        fen = self.board.fen().split()[0]  # Extract FEN string without additional information
        fen_tensor = torch.zeros(1, 64)

        piece_symbols = {
            'P': 1, 'N': 2, 'B': 3, 'R': 4, 'Q': 5, 'K': 6,
            'p': -1, 'n': -2, 'b': -3, 'r': -4, 'q': -5, 'k': -6,
        }

        for i, char in enumerate(fen):
            if char.isalpha():
                piece_value = piece_symbols[char]
                fen_tensor[0, i] = piece_value

        return fen_tensor



if __name__ == "__main__":
    env = ChessEnvironment()
    start = time.time()

    i = 0
    for j in range(2):
        state = env.reset()
        done = False
        while not done:
            # move = env.random_move()
            move = env.engine_move()
            next_state, reward, done = env.step(move)
            state = next_state
            env.save_game_frames(f'frames_{j}')
            if reward != 0.0:
                i += 1
        # env.create_animation(f'frames_{j}', f'game_{j}.gif', delay=100)
    end = time.time()
    print(f'{i} games won in {j+1} games')
    print(f"{j+1} Games took: {end - start} seconds")
