import numpy as np
import matplotlib.pyplot as plt
#plt.style.use('./deeplearning.mplstyle')
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Input
from sklearn.datasets import make_blobs


#NumPy implementation of softmax
def my_softmax(z):
    ez = np.exp(z)              #element-wise exponenial
    sm = ez/np.sum(ez)
    return(sm)


#Let's start by creating a dataset to train a multiclass classification model.
# make  dataset for example
centers = [[-5, 2], [-2, -2], [1, 2], [5, -2]]
X_train, y_train = make_blobs(n_samples=2000, centers=centers, cluster_std=1.0,random_state=30)

#The model below is implemented with the softmax as an 
# activation in the final Dense layer. 
# The loss function is separately specified in the compile directive.
#The loss function is SparseCategoricalCrossentropy

model = Sequential(
    [ 
        #Input(shape=X_train),
        Dense(25, activation = 'relu'),
        Dense(15, activation = 'relu'),
        Dense(4, activation = 'softmax')    # < softmax activation here
    ]
)
model.compile(
    loss=tf.keras.losses.SparseCategoricalCrossentropy(),
    optimizer=tf.keras.optimizers.Adam(0.001),
)

model.fit(
    X_train,y_train,
    epochs=10
)

#Because the softmax is integrated into the output layer, 
# the output is a vector of probabilities.
p_nonpreferred = model.predict(X_train)
print(p_nonpreferred [:2])
print("largest value", np.max(p_nonpreferred), "smallest value", np.min(p_nonpreferred))


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#more stable and accurate results can be obtained if the softmax and loss are combined during training
#In the preferred organization the final layer has a linear activation
#he loss function has an additional argument: from_logits = True
#This informs the loss function that the softmax operation should be included in the loss calculation
preferred_model = Sequential(
    [ 
        Dense(25, activation = 'relu'),
        Dense(15, activation = 'relu'),
        Dense(4, activation = 'linear')   #<-- Note
    ]
)
preferred_model.compile(
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),  #<-- Note
    optimizer=tf.keras.optimizers.Adam(0.001),
)

preferred_model.fit(
    X_train,y_train,
    epochs=10
)

p_preferred = preferred_model.predict(X_train)
print(f"two example output vectors:\n {p_preferred[:2]}")
print("largest value", np.max(p_preferred), "smallest value", np.min(p_preferred))

#The output predictions are not probabilities! 
# If the desired output are probabilities, the output should be be processed by a softmax.
sm_preferred = tf.nn.softmax(p_preferred).numpy()
print(f"two example output vectors:\n {sm_preferred[:2]}")
print("largest value", np.max(sm_preferred), "smallest value", np.min(sm_preferred))

#To select the most likely category, the softmax is not required. 
# One can find the index of the largest output using np.argmax().
for i in range(5):
    print( f"{p_preferred[i]}, category: {np.argmax(p_preferred[i])}")

#########
#SparseCategorialCrossentropy or CategoricalCrossEntropy

# SparseCategorialCrossentropy: expects the target to be an integer corresponding to the index. 
# For example, if there are 10 potential target values, y would be between 0 and 9.

# CategoricalCrossEntropy: Expects the target value of an example to be one-hot encoded where 
# the value at the target index is 1 while the other N-1 entries are zero. 
# An example with 10 potential target values, where the target is 2 would be [0,0,1,0,0,0,0,0,0,0].