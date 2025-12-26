import numpy as np
import tensorflow as tf
from tensorflow import keras


# The goal of a collaborative filtering recommender system is to generate two vectors: 
# For each user, a 'parameter vector' that embodies the movie tastes of a user. 
# For each movie, a feature vector of the same size which embodies some description of the movie. 
# The dot product of the two vectors plus the bias 
# term should produce an estimate of the rating the user might give to that movie.


# The collaborative filtering algorithm in the setting of movie recommendations considers a set of  𝑛
# -dimensional parameter vectors  𝐱(0),...,𝐱(𝑛𝑚−1),  𝐰(0),...,𝐰(𝑛𝑢−1)
#   and  𝑏(0),...,𝑏(𝑛𝑢−1)
#  , where the model predicts the rating for movie  𝑖
#   by user  𝑗
#   as  𝑦(𝑖,𝑗)=𝐰(𝑗)⋅𝐱(𝑖)+𝑏(𝑗)
#   . Given a dataset that consists of a set of ratings produced by some users on some movies, 
#   you wish to learn the parameter vectors  𝐱(0),...,𝐱(𝑛𝑚−1),𝐰(0),...,𝐰(𝑛𝑢−1)
#   and  𝑏(0),...,𝑏(𝑛𝑢−1)
#   that produce the best fit (minimizes the squared error).

def cofi_cost_func(X, W, b, Y, R, lambda_):
    """
    Returns the cost for the content-based filtering
    Args:
      X (ndarray (num_movies,num_features)): matrix of item features
      W (ndarray (num_users,num_features)) : matrix of user parameters
      b (ndarray (1, num_users)            : vector of user parameters
      Y (ndarray (num_movies,num_users)    : matrix of user ratings of movies
      R (ndarray (num_movies,num_users)    : matrix, where R(i, j) = 1 if the i-th movies was rated by the j-th user
      lambda_ (float): regularization parameter
    Returns:
      J (float) : Cost
    """
    nm, nu = Y.shape
    J = 0
    ### START CODE HERE ###  
    for j in range(nu):
        w = W[j,:]
        b_j = b[0,j]
        for i in range(nm):
            if R[i,j] == 1:
                x = X[i]
                y = Y[i,j]
               # r =
                J += np.square((np.dot(w,x) + b_j - y ))
                #((W[j] * X[i] + b[j]) - Y[i,j])**2
    J = J/2
    J += (lambda_/2) * (np.sum(np.square(W)) + np.sum(np.square(X)))
    ### END CODE HERE ### 

    return J


#=================================================================================================================================================
#Vectorized Implementation
# It is important to create a vectorized implementation to compute  𝐽
#  , since it will later be called many times during optimization.
def cofi_cost_func_v(X, W, b, Y, R, lambda_):
    """
    Returns the cost for the content-based filtering
    Vectorized for speed. Uses tensorflow operations to be compatible with custom training loop.
    Args:
      X (ndarray (num_movies,num_features)): matrix of item features
      W (ndarray (num_users,num_features)) : matrix of user parameters
      b (ndarray (1, num_users)            : vector of user parameters
      Y (ndarray (num_movies,num_users)    : matrix of user ratings of movies
      R (ndarray (num_movies,num_users)    : matrix, where R(i, j) = 1 if the i-th movies was rated by the j-th user
      lambda_ (float): regularization parameter
    Returns:
      J (float) : Cost
    """
    j = (tf.linalg.matmul(X, tf.transpose(W)) + b - Y)*R
    J = 0.5 * tf.reduce_sum(j**2) + (lambda_/2) * (tf.reduce_sum(X**2) + tf.reduce_sum(W**2))
    return J


# Let's now train the collaborative filtering model. This will learn the parameters  𝐗,  𝐖, and  𝐛.
# The operations involved in learning 𝑤, 𝑏, and 𝑥
#  simultaneously do not fall into the typical 'layers' offered in the TensorFlow neural network package. 
#  Consequently, the flow used in Course 2: Model, Compile(), Fit(), Predict(), 
#  are not directly applicable. Instead, we can use a custom training loop.

# Recall from earlier labs the steps of gradient descent.
# *repeat until convergence:
#  *compute forward pass
#  *compute the derivatives of the loss relative to parameters
#  *update the parameters using the learning rate and the computed derivatives

# TensorFlow has the marvelous capability of calculating the derivatives for you. 
# This is shown below. Within the tf.GradientTape() section, 
# operations on Tensorflow Variables are tracked. When tape.
# gradient() is later called, it will return the gradient of the loss relative to the tracked variables. 
# The gradients can then be applied to the parameters using an optimizer
iterations = 200
lambda_ = 1
for iter in range(iterations):
    # Use TensorFlow’s GradientTape
    # to record the operations used to compute the cost 
    with tf.GradientTape() as tape:

        # Compute the cost (forward pass included in cost)
        cost_value = cofi_cost_func_v(X, W, b, Ynorm, R, lambda_)

    # Use the gradient tape to automatically retrieve
    # the gradients of the trainable variables with respect to the loss
    grads = tape.gradient( cost_value, [X,W,b] )

    # Run one step of gradient descent by updating
    # the value of the variables to minimize the loss.
    optimizer.apply_gradients( zip(grads, [X,W,b]) )

    # Log periodically.
    if iter % 20 == 0:
        print(f"Training loss at iteration {iter}: {cost_value:0.1f}")