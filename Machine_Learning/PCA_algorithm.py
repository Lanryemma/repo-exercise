import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

#We are going work on the same example that Andrew has shown in the lecture.
X = np.array([[ 99,  -1],
       [ 98,  -1],
       [ 97,  -2],
       [101,   1],
       [102,   1],
       [103,   2]])

# Loading the PCA algorithm
pca_2 = PCA(n_components=2)
print(pca_2)

# Let's fit the data. We do not need to scale it, since sklearn's implementation already handles it.
pca_2.fit(X)

print(pca_2.explained_variance_ratio_)

# The coordinates on the first principal component (first axis) are enough to retain 99.24% of 
# the information ("explained variance").The second principal component adds an additional
# 0.76% of the information ("explained variance") that is not stored in the first principal component coordinates.
X_trans_2 = pca_2.transform(X)
print(X_trans_2)

# Think of column 1 as the coordinate along the first principal component (the first new axis) and column 2 as 
# the coordinate along the second principal component (the second new axis).

#==========================================================================================================================
#You can probably just choose the first principal component since it retains 99% of the information (explained variance).
pca_1 = PCA(n_components=1)
print(pca_1)

pca_1.fit(X)
print(pca_1.explained_variance_ratio_)

X_trans_1 = pca_1.transform(X)
print(X_trans_1)

#Notice how this column is just the first column of X_trans_2.

#If you had 2 features (two columns of data) and choose 2 principal components, 
# then you'll keep all the information and the data will end up the same as the original.
X_reduced_2 = pca_2.inverse_transform(X_trans_2)
print(f'the reversed version of X_trans_2 is  {X_reduced_2}')