import chess
import random
import chess.svg
import subprocess
import os
import time


class ChessEnvironment:
    def __init__(self):
        self.board = chess.Board()
        self.svg_frames = []

    def reset(self):
        self.board.reset()
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
            done = True
        else:
            reward = 0.0
            done = False

        return self.board.fen(), reward, done

    def legal_moves(self):
        return list(self.board.legal_moves)

    def random_move(self):
        move = random.choice(list(self.board.legal_moves))
        return move

    def engine_move(self):
        result = self.engine.play(self.board, chess.engine.Limit(time=2.0))
        move = result.move
        return move

    def render(self):
        print(self.board)

    def save_game_frames(self, directory):
        svg = chess.svg.board(board=self.board)
        self.svg_frames.append(svg)

        if done:
            # Create the frames directory if it doesn't exist
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Save each SVG frame to a separate file
            for i, svg in enumerate(self.svg_frames):
                frame_path = os.path.join(directory, f'frame_{i}.svg')
                with open(frame_path, 'w') as f:
                    f.write(svg)

    def create_animation(self, frames_directory, output_filename, delay=100):
        # Convert SVG frames to PNG
        subprocess.run(['convert', '-delay', str(delay), f'{frames_directory}/*.svg', output_filename])

if __name__ == "__main__":
   
    env = ChessEnvironment()

    # time how long it takes to play a game
    
    start = time.time()

    # play multiple games
    for j in range(1000):


        state = env.reset()
        # env.render()
        done = False
        i = 0
        while not done:
            i += 1
            move = env.random_move()
            next_state, reward, done = env.step(move)

            state = next_state

            # env.render()
            # env.save_game_frames(f'frames_{i}')

        

        

        # Create an animated GIF from the SVG frames
        # env.create_animation('frames_{i}', "game_{i}.gif", delay=100)

    end = time.time()
    # print with format
    print(f"{j+1} Games took: {end - start} seconds")
