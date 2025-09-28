import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
#from lab_coffee_utils import load_coffee_data
import matplotlib.pyplot as plt

# Simulate the coffee data loading (since we can't import lab_coffee_utils)
# def load_coffee_data():
#     # This is simulated data - replace with your actual data loading
#     X = np.array([[200, 13.9], [214, 16.4], [200, 17], [198, 15.2], 
#                   [240, 14.4], [234, 16.4], [220, 15.0], [200, 14.5]])
#     Y = np.array([[1], [1], [0], [1], [1], [1], [1], [0]])  # 1=good, 0=bad
#     return X, Y

# Simple plotting function to replace plt_roast
def plot_coffee_data(X, Y):
    plt.figure(figsize=(8, 6))
    plt.scatter(X[Y[:,0] == 1, 0], X[Y[:,0] == 1, 1], marker='x', color='red', label='Good Roast')
    plt.scatter(X[Y[:,0] == 0, 0], X[Y[:,0] == 0, 1], marker='o', color='blue', label='Bad Roast')
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Duration (minutes)')
    plt.title('Coffee Roasting Data')
    plt.legend()
    plt.grid(True)
    plt.show()

def load_coffee_data():
    """ Creates a coffee roasting data set.
        roasting duration: 12-15 minutes is best
        temperature range: 175-260C is best
    """
    rng = np.random.default_rng(2)
    X = rng.random(400).reshape(-1,2)
    X[:,1] = X[:,1] * 4 + 11.5          # 12-15 min is best
    X[:,0] = X[:,0] * (285-150) + 150  # 350-500 F (175-260 C) is best
    Y = np.zeros(len(X))
    
    i=0
    for t,d in X:
        y = -3/(260-175)*t + 21
        if (t > 175 and t < 260 and d > 12 and d < 15 and d<=y ):
            Y[i] = 1
        else:
            Y[i] = 0
        i += 1

    return (X, Y.reshape(-1,1))
# Load and plot data
X, Y = load_coffee_data()
print(f"X shape: {X.shape}, Y shape: {Y.shape}")
plot_coffee_data(X, Y)

# Convert to PyTorch tensors
X_tensor = torch.tensor(X, dtype=torch.float32)
Y_tensor = torch.tensor(Y, dtype=torch.float32)

# Normalize data
print(f"Temperature Max, Min pre normalization: {np.max(X[:,0]):0.2f}, {np.min(X[:,0]):0.2f}")
print(f"Duration    Max, Min pre normalization: {np.max(X[:,1]):0.2f}, {np.min(X[:,1]):0.2f}")

mean = X_tensor.mean(dim=0)
std = X_tensor.std(dim=0)
Xn = (X_tensor - mean) / std

#print(f"Temperature Max, Min post normalization: {np.max(Xn[:,0]):0.2f}, {np.min(Xn[:,0]):0.2f}")
#print(f"Duration    Max, Min post normalization: {np.max(Xn[:,1]):0.2f}, {np.min(Xn[:,1]):0.2f}")

# FIXED: Use PyTorch methods for PyTorch tensors
print(f"Temperature Max, Min post normalization: {Xn[:,0].max().item():0.2f}, {Xn[:,0].min().item():0.2f}")
print(f"Duration    Max, Min post normalization: {Xn[:,1].max().item():0.2f}, {Xn[:,1].min().item():0.2f}")

# Expand data
Xt = Xn.repeat(1000, 1)
Yt = Y_tensor.repeat(1000, 1)
print(f"Xt shape: {Xt.shape}, Yt shape: {Yt.shape}")

# Set random seed
torch.manual_seed(1234)

# Define model
model = nn.Sequential(
    nn.Linear(2, 3),
    nn.Sigmoid(),
    nn.Linear(3, 1),
    nn.Sigmoid()
)

print(f"L1 params: {2 * 3 + 3}, L2 params: {3 * 1 + 1}")

# Training
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

print("Training...")
for epoch in range(10):
    predictions = model(Xt)
    loss = criterion(predictions, Yt)
    
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    if (epoch + 1) % 2 == 0:
        print(f'Epoch [{epoch+1}/10], Loss: {loss.item():.4f}')

# Test predictions
X_test = np.array([[200, 13.9], [200, 17]])
X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
X_testn = (X_test_tensor - mean) / std

model.eval()
with torch.no_grad():
    predictions = model(X_testn)
    print("\nPredictions = \n", predictions.numpy())
    
    decisions = (predictions >= 0.5).int()
    print(f"Decisions = \n{decisions.numpy()}")