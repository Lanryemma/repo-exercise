import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from keras.layers import Dense, Input
from keras.models import Sequential
from keras.losses import MeanSquaredError, BinaryCrossentropy
from keras.activations import sigmoid
from lab_coffee_utils import load_coffee_data, plt_roast, plt_prob, plt_layer, plt_network, plt_output_unit

#.venv\Scripts\activate
# Press Ctrl+Shift+P

# Type "Python: Select Interpreter"

# Choose the correct Python 3.12.8 installation

# Or select "Enter interpreter path" and browse to your Python 3.12.8 executable

X,Y = load_coffee_data()
print(X.shape, Y.shape)

#Let's plot the coffee roasting data below.
plt_roast(X,Y)

# Normalize Data
# Fitting the weights to the data (back-propagation, covered in next week's lectures) 
# will proceed more quickly if the data is normalized.The procedure below uses a Keras normalization layer.
print(f"Temperature Max, Min pre normalization: {np.max(X[:,0]):0.2f}, {np.min(X[:,0]):0.2f}")
print(f"Duration    Max, Min pre normalization: {np.max(X[:,1]):0.2f}, {np.min(X[:,1]):0.2f}")
norm_l = tf.keras.layers.Normalization(axis=-1)
norm_l.adapt(X)  # learns mean, variance
Xn = norm_l(X)
print(f"Temperature Max, Min post normalization: {np.max(Xn[:,0]):0.2f}, {np.min(Xn[:,0]):0.2f}")
print(f"Duration    Max, Min post normalization: {np.max(Xn[:,1]):0.2f}, {np.min(Xn[:,1]):0.2f}")

#Tile/copy our data to increase the training set size and reduce the number of training epochs.
Xt = np.tile(Xn,(1000,1))
Yt= np.tile(Y,(1000,1))   
print(Xt.shape, Yt.shape)   

tf.random.set_seed(1234)  # applied to achieve consistent results
model = Sequential(
    [
        tf.keras.Input(shape=(2,)),
        Dense(3, activation='sigmoid', name = 'layer1'),
        Dense(1, activation='sigmoid', name = 'layer2')
     ]
)

#The model.summary() provides a description of the network:
#The parameter counts shown in the summary correspond to the number of 
# elements in the weight and bias arrays as shown below.
L1_num_params = 2 * 3 + 3   # W1 parameters  + b1 parameters
L2_num_params = 3 * 1 + 1   # W2 parameters  + b2 parameters
print("L1 params = ", L1_num_params, ", L2 params = ", L2_num_params  )

# In the first layer with 3 units, we expect W to have a size of (2,3) and  𝑏
#   should have 3 elements.
# In the second layer with 1 unit, we expect W to have a size of (3,1) and  𝑏
#   should have 1 element.

W1, b1 = model.get_layer("layer1").get_weights()
W2, b2 = model.get_layer("layer2").get_weights()
print(f"W1{W1.shape}:\n", W1, f"\nb1{b1.shape}:", b1)
print(f"W2{W2.shape}:\n", W2, f"\nb2{b2.shape}:", b2)


# The following statements will be described in detail in Week2. For now:
# The model.compile statement defines a loss function and specifies a compile optimization.
# The model.fit statement runs gradient descent and fits the weights to the data.

model.compile(
    loss = tf.keras.losses.BinaryCrossentropy(),
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.01),
)

model.fit(
    Xt,Yt,            
    epochs=10,
)

# Epochs and batches
# In the fit statement above, the number of epochs was set to 10. 
# This specifies that the entire data set should be applied during training 10 times.
# The first line, Epoch 1/10, describes which epoch the model is currently running. 
# For efficiency, the training data set is broken into 'batches'. 
# The default size of a batch in Tensorflow is 32. There are 200000 examples in our expanded data set or 6250 batches. 
# The notation on the 2nd line 6250/6250 [==== is describing which batch has been executed.

# Updated Weights
# After fitting, the weights have been updated
W1, b1 = model.get_layer("layer1").get_weights()
W2, b2 = model.get_layer("layer2").get_weights()
print("W1:\n", W1, "\nb1:", b1)
print("W2:\n", W2, "\nb2:", b2)


# You can see that the values are different from what you printed before calling model.fit().
# With these, the model should be able to discern what is a good or bad coffee roast.
# After finishing the lab later, you can re-run all 
# cells except this one to see if your trained model
# gets the same results.

# Set weights from a previous run. 
W1 = np.array([
    [-8.94,  0.29, 12.89],
    [-0.17, -7.34, 10.79]] )
b1 = np.array([-9.87, -9.28,  1.01])
W2 = np.array([
    [-31.38],
    [-27.86],
    [-32.79]])
b2 = np.array([15.54])

# Replace the weights from your trained model with
# the values above.
# model.get_layer("layer1").set_weights([W1,b1])
# model.get_layer("layer2").set_weights([W2,b2])


# Let's start by creating input data. 
# The model is expecting one or more examples where examples are in the rows of matrix. 
# In this case, we have two features so the matrix will be (m,2) where m is the number of examples. 
# Recall, we have normalized the input features so we must normalize our test data as well.
# To make a prediction, you apply the predict method.
X_test = np.array([
    [200,13.9],  # positive example
    [200,17]])   # negative example
X_testn = norm_l(X_test)
predictions = model.predict(X_testn)
print("predictions = \n", predictions)

#To convert the probabilities to a decision, we apply a threshold:
yhat = np.zeros_like(predictions)
for i in range(len(predictions)):
    if predictions[i] >= 0.5:
        yhat[i] = 1
    else:
        yhat[i] = 0
print(f"decisions = \n{yhat}")


#This can be accomplished more succinctly:
yhat = (predictions >= 0.5).astype(int)
print(f"decisions = \n{yhat}")


#===============================================================================================================================
#if we are to see how the dense function,prediction function and 
# the sequential functions work behind the scenes we can see it here
# Define the activation function
g = sigmoid

def my_dense(a_in, W, b):
    """
    Computes dense layer
    Args:
      a_in (ndarray (n, )) : Data, 1 example 
      W    (ndarray (n,j)) : Weight matrix, n features per unit, j units
      b    (ndarray (j, )) : bias vector, j units  
    Returns
      a_out (ndarray (j,))  : j units|
    """
    units = W.shape[1]
    a_out = np.zeros(units)
    for j in range(units):               
        w = W[:,j]                                    
        z = np.dot(w, a_in) + b[j]         
        a_out[j] = g(z)               
    return(a_out)


def my_sequential(x, W1, b1, W2, b2):
    a1 = my_dense(x,  W1, b1)
    a2 = my_dense(a1, W2, b2)
    return(a2)

#We can copy trained weights and biases from the previous lab in Tensorflow.
W1_tmp = np.array( [[-8.93,  0.29, 12.9 ], [-0.1,  -7.32, 10.81]] )
b1_tmp = np.array( [-9.82, -9.28,  0.96] )
W2_tmp = np.array( [[-31.18], [-27.59], [-32.56]] )
b2_tmp = np.array( [15.41] )


def my_predict(X, W1, b1, W2, b2):
    m = X.shape[0]
    p = np.zeros((m,1))
    for i in range(m):
        p[i,0] = my_sequential(X[i], W1, b1, W2, b2)
    return(p)


#We can try this routine on two examples:
X_tst = np.array([
    [200,13.9],  # postive example
    [200,17]])   # negative example
X_tstn = norm_l(X_tst)  # remember to normalize
predictions = my_predict(X_tstn, W1_tmp, b1_tmp, W2_tmp, b2_tmp)

#To convert the probabilities to a decision, we apply a threshold:
yhat = np.zeros_like(predictions)
for i in range(len(predictions)):
    if predictions[i] >= 0.5:
        yhat[i] = 1
    else:
        yhat[i] = 0
print(f"decisions = \n{yhat}")

#This can be accomplished more succinctly:
yhat = (predictions >= 0.5).astype(int)
print(f"decisions = \n{yhat}")