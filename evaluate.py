import chess
import torch
import chess.svg
from environment import ChessEnvironment
from model import ChessNet

model = ChessNet()
model.load_state_dict(torch.load('chess_net.pth'))
model.eval()

# Create an instance of the ChessEnvironment


class Evaluation:
    def __init__(self):
        pass
    def self_play(self, number_of_games):
        env = ChessEnvironment()
        for game_number in range(number_of_games):
            state = env.reset()
            done = False

            while not done:
                # Select the best move
                fen_tensor = env.get_fen_tensor()
                output = model(fen_tensor)
                action_index = torch.argmax(output).item()
                legal_moves = env.legal_moves()
                move = legal_moves[action_index]

                # Make the move
                next_state, reward, done = env.step(move)
                
                # Save the SVG file
                env.save_game_frames(f"game_self_{game_number+1}")

                if done:
                    break
            print(f"Game {game_number+1} finished. Result: {env.board.result()}")
    
    def play_against_stockfish(self, number_of_games, stockfish_depth=10):
        env = ChessEnvironment(stockfish_depth=stockfish_depth)
        for game_number in range(number_of_games):
            state = env.reset()
            done = False
            round = 0
            while not done:
                if round % 2 == 0:
                    # Player's turn
                    fen_tensor = env.get_fen_tensor()
                    output = model(fen_tensor)
                    action_index = torch.argmax(output).item()
                    legal_moves = env.legal_moves()
                    move = legal_moves[action_index]
                else:
                    # Stockfish's turn
                    move = env.engine_move()

                # Make the move
                next_state, reward, done = env.step(move)

                # Save the SVG file
                env.save_game_frames(f"game_stockfish_{game_number+1}")

                if done:
                    break
                round += 1

            print(f"Game {game_number+1} finished. Result: {env.board.result()}")


if __name__ == "__main__":
    evaluation = Evaluation()
    evaluation.self_play(1)
    evaluation.play_against_stockfish(1, stockfish_depth=1)
    