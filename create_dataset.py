import chess.pgn
import json

pgn_file_path = 'lichess_.pgn'
json_file_path = 'moves.json'

games = []

with open(pgn_file_path) as pgn_file:
    while True:
        game = chess.pgn.read_game(pgn_file)
        if game is None:
            break

        move_list = [str(move) for move in game.mainline_moves()]
        result = game.headers['Result']
        game_data = {'moves': move_list, 'result': result}
        games.append(game_data)

# Save the games to a JSON file
with open(json_file_path, 'w') as json_file:
    json.dump(games, json_file)
