import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#Decision Trees

# We will use one-hot encoding to encode the categorical features. They will be as follows:

# Ear Shape: Pointy = 1, Floppy = 0
# Face Shape: Round = 1, Not Round = 0
# Whiskers: Present = 1, Absent = 0

# Therefore, we have two sets:

# X_train: for each example, contains 3 features:

#       - Ear Shape (1 if pointy, 0 otherwise)
#       - Face Shape (1 if round, 0 otherwise)
#       - Whiskers (1 if present, 0 otherwise)
# y_train: whether the animal is a cat

#       - 1 if the animal is a cat
#       - 0 otherwise

X_train = np.array([[1, 1, 1],
[0, 0, 1],
 [0, 1, 0],
 [1, 0, 1],
 [1, 1, 1],
 [1, 1, 0],
 [0, 0, 0],
 [1, 1, 0],
 [0, 1, 0],
 [0, 1, 0]])

y_train = np.array([1, 1, 0, 0, 1, 1, 0, 1, 0, 0])

#For instance, the first example
print(X_train[0])
#array([1, 1, 1])
#This means that the first example has a pointy ear shape, round face shape and it has whiskers.


# On each node, we compute the information gain for each feature, 
# then split the node on the feature with the higher information gain, 
# by comparing the entropy of the node with the weighted entropy in the two splitted nodes.

#Now let's write a function to compute the entropy.

def entropy(p):
    if p == 0 or p == 1:
        return 0
    else:
        return -p * np.log2(p) - (1- p)*np.log2(1 - p)
        
print(entropy(0.5))

#To illustrate, let's compute the information gain if we split the node for each of the features. 
# To do this, let's write some functions.
def split_indices(X, index_feature):
    """Given a dataset and a index feature, return two lists for the two split nodes, 
    the left node has the animals that have 
    that feature = 1 and the right node those that have the feature = 0 
    index feature = 0 => ear shape
    index feature = 1 => face shape
    index feature = 2 => whiskers
    """
    left_indices = []
    right_indices = []
    for i,x in enumerate(X):
        if x[index_feature] == 1:
            left_indices.append(i)
        else:
            right_indices.append(i)
    return left_indices, right_indices

# So, if we choose Ear Shape to split, 
# then we must have in the left node (check the table above) the indices: 03457
# and the right indices, the remaining ones.

split_indices(X_train, 0)
#([0, 3, 4, 5, 7], [1, 2, 6, 8, 9])

# Now we need another function to compute the weighted entropy in the splitted nodes. 
# As you've seen in the video lecture, we must find:

# 𝑤 left and  𝑤 right, the proportion of animals in each node.
# 𝑝 left and  𝑝 right, the proportion of cats in each split.

#Note the difference between these two definitions!! To illustrate, 
# if we split the root node on the feature of index 0 (Ear Shape), 
# then in the left node, the one that has the animals 0, 3, 4, 5 and 7, we have:

# 𝑤 left=5/10=0.5 and 𝑝 left=4/5
# 𝑤 right=5/10=0.5 and 𝑝 right=1/5

def weighted_entropy(X,y,left_indices,right_indices):
    """
    This function takes the splitted dataset, the indices we chose to split and returns the weighted entropy.
    """
    w_left = len(left_indices)/len(X)
    w_right = len(right_indices)/len(X)
    p_left = sum(y[left_indices])/len(left_indices)
    p_right = sum(y[right_indices])/len(right_indices)
    
    weighted_entropy = w_left * entropy(p_left) + w_right * entropy(p_right)
    return weighted_entropy

left_indices, right_indices = split_indices(X_train, 0)
weighted_entropy(X_train, y_train, left_indices, right_indices)

# So, the weighted entropy in the 2 split nodes is 0.72. 
# To compute the Information Gain we must subtract it from the 
# entropy in the node we chose to split (in this case, the root node).

def information_gain(X, y, left_indices, right_indices):
    """
    Here, X has the elements in the node and y is theirs respectives classes
    """
    p_node = sum(y)/len(y)
    h_node = entropy(p_node)
    w_entropy = weighted_entropy(X,y,left_indices,right_indices)
    return h_node - w_entropy

information_gain(X_train, y_train, left_indices, right_indices)

#Now, let's compute the information gain if we split the root node for each feature:
for i, feature_name in enumerate(['Ear Shape', 'Face Shape', 'Whiskers']):
    left_indices, right_indices = split_indices(X_train, i)
    i_gain = information_gain(X_train, y_train, left_indices, right_indices)
    print(f"Feature: {feature_name}, information gain if we split the root node using this feature: {i_gain:.2f}")