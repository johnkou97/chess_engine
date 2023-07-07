# Chess Engine using Supervised Learning

## Introduction

This is a chess engine that uses supervised learning to play chess. It is written in Python and uses the [python-chess](https://python-chess.readthedocs.io/en/latest/) library to handle chess board and move representation.

## Files

- `environment.py`: Contains the `ChessEnvironment` class, which is used to represent the chess board and the current state of the game. 
- `create_dataset.py`: Creates a dataset of chess board positions and the best move to make in that position. This dataset is used to train the neural network model.
- `model.py`: Contains the `ChessNet` class, which is used to represent the neural network model being used to predict the best move.
- `helper.py`: Contains helper functions used to convert between chess board representations and neural network inputs.
- `train.py`: Handles the training of the neural network model.
- `evaluate.py`: Evaluates the performance of the neural network model by playing against it using self-play or against a stockfish engine.

## Usage

Run `create_dataset.py` to create a dataset of chess board positions. This dataset is used to train the neural network model. Then, run `train.py` to train the neural network model. Finally, run `evaluate.py` to evaluate the performance of the neural network model.


