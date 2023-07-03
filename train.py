import json
import torch
import torch.nn as nn
import torch.optim as optim
from environment import ChessEnvironment
from model import ChessNet
from helper import move_to_input, result_to_target

json_file_path = 'moves.json'

with open(json_file_path) as json_file:
    games = json.load(json_file)

env = ChessEnvironment()

# Load the game data and prepare the input and target tensors
with open(json_file_path) as json_file:
    games = json.load(json_file)

input_data = []
target_data = []

for game in games:
    moves = game['moves']
    result = game['result']

    for move in moves:
        # Convert move to input and target tensors
        input_tensor = torch.tensor(move_to_input(move))  # Implement move_to_input() function to convert move to input tensor
        target_tensor = torch.tensor(result_to_target(result))  # Implement move_to_target() function to convert result to target tensor

        # Convert target tensor to long datatype


        input_data.append(input_tensor)
        target_data.append(target_tensor)

# Create the ChessNet model
model = ChessNet()

# Define the loss function and optimizer
criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)

num_epochs = 1

# Train the network
for epoch in range(num_epochs):
    running_loss = 0.0
    for input_tensor, target_tensor in zip(input_data, target_data):
        # Zero the gradients
        optimizer.zero_grad()
    
        # Forward pass
        output = model(input_tensor)

        # Compute the loss
        loss = criterion(output, target_tensor)

        # Backward pass
        loss.backward()

        # Update the weights
        optimizer.step()

        running_loss += loss.item()

    # Print the loss for this epoch
    print(f"Epoch {epoch+1} Loss: {running_loss}")

# Save the trained model
torch.save(model.state_dict(), "chess_net.pth")   
    