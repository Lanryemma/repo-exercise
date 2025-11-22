import numpy as np
import matplotlib.pyplot as plt

# Finding closest centroids
# In the “cluster assignment” phase of the K-means algorithm, 
# the algorithm assigns every training example  𝑥(𝑖)
#   to its closest centroid, given the current positions of centroids.

X = np.array([[ 1.84207953, 4.6075716 ],
 [ 5.65858312,  4.79996405],
 [ 6.35257892,  3.2908545 ],
 [ 2.90401653,  4.61220411], 
 [ 3.23197916,  4.93989405],
 [ 1.24792268,  4.93267846],
 [ 1.97619886,  4.43489674],
 [ 2.23454135, 5.05547168],
 [ 2.98340757 , 4.84046406],
 [ 2.97970391 , 4.80671081],
 [ 2.11496411 , 5.37373587],
 [ 2.12169543 , 5.20854212],
 [ 1.5143529  , 4.77003303],
 [ 2.16979227 , 5.27435354],
 [ 0.41852373 , 4.88312522],
 [ 2.47053695 , 4.80418944],
 [ 4.06069132 , 4.99503862],
 [ 3.00708934 , 4.67897758],
 [ 0.66632346 , 4.87187949],
 [ 3.1621865  , 4.83658301],
 [ 0.51155258 , 4.91052923],
 [ 3.1342801 ,  4.96178114],
 [ 2.04974595 , 5.6241395 ],
 [ 0.66582785 , 5.24399257],
 [ 1.01732013, 4.84473647],
 [ 2.17893568 , 5.29758701],
 [ 2.85962615, 5.26041997],
 [ 1.30882588, 5.30158701],
 [ 0.99253246, 5.01567424],
 [ 1.40372638, 4.57527684],
 [ 2.66046572, 5.19623848],
 [ 2.79995882,  5.11526323],
 [ 2.06995345 , 4.6846713 ],
 [ 3.29765181 , 5.59205535],
 [ 1.8929766  , 4.89043209],
 [ 2.55983064 , 5.26397756],
 [ 1.15354031 , 4.67866717],
 [ 2.25150754 , 5.4450031 ],
 [ 2.20960296 , 4.91469264],
 [ 1.59141937 , 4.83212573],
 [ 1.67838038 , 5.26903822],
 [ 2.59148642 , 4.92593394],
 [ 2.80996442 , 5.53849899],
 [ 0.95311627 , 5.58037108],
 [ 1.51775276 , 5.03836638],
 [ 3.23114248 , 5.78429665],
 [ 2.54180011 , 4.81098738],
 [ 3.81422865 , 4.73526796],
 [ 1.68495829 , 4.59643553],
 [ 2.17777173 , 4.86154019],
 [ 1.8173328  , 5.13333907],
 [ 1.85776553 , 4.86962414],
 [ 3.03084301 , 5.24057582],
 [ 2.92658295 , 5.09667923],
 [ 3.43493543 , 5.34080741],
 [ 3.20367116 , 4.85924759],
 [ 0.10511804 , 4.72916344],
 [ 1.40597916 , 5.06636822],
 [ 2.24185052 , 4.9244617 ],
 [ 1.36678395 , 5.26161095],
 [ 1.70725482 , 4.04231479],
 [ 1.91909566 , 5.57848447],
 [ 1.60156731 , 4.64453012],
 [ 0.37963437 , 5.26194729],
 [ 2.02134502 , 4.41267445],
 [ 1.12036737 , 5.20880747],
 [ 2.26901428 , 4.61818883],
 [-0.24512713 , 5.74019237],
 [ 2.12857843 , 5.01149793],
 [ 1.84419981 , 5.03153948],
 [ 2.32558253 , 4.74867962],
 [ 1.52334113 , 4.87916159],
 [ 1.02285128 , 5.0105065 ],
 [ 1.85382737 , 5.00752482],
 [ 2.20321658 , 4.94516379],
 [ 1.20099981 , 4.57829763],
 [ 1.02062703 , 4.62991119],
 [ 1.60493227 , 5.13663139],
 [ 0.47647355 , 5.13535977],
 [ 0.3639172  , 4.73332823],
 [ 0.31319845 , 5.54694644],
 [ 2.28664839 , 5.0076699 ],
 [ 2.15460139 , 5.46282959],
 [ 2.05288518 , 4.77958559],
 [ 4.88804332 , 5.50670795],
 [ 2.40304747 , 5.08147326],
 [ 2.56869453 , 5.20687886],
 [ 1.82975993 , 4.59657288],
 [ 0.54845223 , 5.0267298 ],
 [ 3.17109619 , 5.5946452 ],
 [ 3.04202069 , 5.00758373],
 [ 2.40427775 , 5.0258707 ],
 [ 0.17783466 , 5.29765032],
 [ 2.61428678 , 5.22287414],
 [ 2.30097798 , 4.97235844],
 [ 3.90779317 , 5.09464676],
 [ 2.05670542,  5.23391326],
 [ 1.38133497 , 5.00194962],
 [ 1.16074178,  4.67727927],
 [ 1.72818199 , 5.36028437]])

# GRADED FUNCTION: find_closest_centroids

def find_closest_centroids(X, centroids):
    """
    Computes the centroid memberships for every example
    
    Args:
        X (ndarray): (m, n) Input values      
        centroids (ndarray): (K, n) centroids
    
    Returns:
        idx (array_like): (m,) closest centroids
    
    """

    # Set K
    K = centroids.shape[0]

    # You need to return the following variables correctly
    idx = np.zeros(X.shape[0], dtype=int)
    ### START CODE HERE ###
    for i in range(X.shape[0]):
         # Array to hold distance between X[i] and each centroids[j]
        distance = []
        for j in range(centroids.shape[0]):
            # Your code to calculate the norm between (X[i] - centroids[j])
            #You can use np.linalg.norm to calculate the norm
            norm_ij = np.linalg.norm(X[i] - centroids[j])
            distance.append(norm_ij)  
            
        # Your code here to calculate index of minimum value in distance
        # You can use np.argmin to find the index of the minimum value
        idx[i] = np.argmin(distance)
    ### END CODE HERE ###
    
    return idx

# Select an initial set of centroids (3 Centroids)
initial_centroids = np.array([[3,3], [6,2], [8,5]])

# Find closest centroids using initial_centroids
idx = find_closest_centroids(X, initial_centroids)

# Print closest centroids for the first three elements
print("First three elements in idx are:", idx[:3])

#====================================================================================================================================================================

# Computing centroid means
# Given assignments of every point to a centroid, the second phase of the algorithm recomputes, 
# for each centroid, the mean of the points that were assigned to it.

#Say we wanted to find all the values in X that were assigned to cluster k=0
#You can use np.mean to find the mean. Make sure to set the parameter axis=0
# UNQ_C2
# GRADED FUNCTION: compute_centroids

def compute_centroids(X, idx, K):
    """
    Returns the new centroids by computing the means of the 
    data points assigned to each centroid.
    
    Args:
        X (ndarray):   (m, n) Data points
        idx (ndarray): (m,) Array containing index of closest centroid for each 
                       example in X. Concretely, idx[i] contains the index of 
                       the centroid closest to example i
        K (int):       number of centroids
    
    Returns:
        centroids (ndarray): (K, n) New centroids computed
    """
    
    # Useful variables
    m, n = X.shape 
    # You need to return the following variables correctly
    centroids = np.zeros((K, n))
    
    ### START CODE HERE ###
    for k in range(K): 
        points = X[idx == k]
#         points = []
#         for i in range(m)
#             if idx[i] == k:
#                 points.append(i)
                
        # Your code here to get a list of all data points in X assigned to centroid k  
        centroids[k] = np.mean(points, axis = 0)
        # Your code here to compute the mean of the points assigned
    ### END CODE HERE ## 
    
    return centroids

#Now check your implementation by running the cell below
K = 3
centroids = compute_centroids(X, idx, K)
print("The centroids are:", centroids)

#===========================================================================================================================================================

# K-means on a sample dataset
# After you have completed the two functions (find_closest_centroids and compute_centroids) above, 
# the next step is to run the K-means algorithm on a toy 2D dataset to help you understand how K-means works.
# You do not need to implement anything for this part

def run_kMeans(X, initial_centroids, max_iters=10, plot_progress=False):
    """
    Runs the K-Means algorithm on data matrix X, where each row of X
    is a single example
    """
    
    # Initialize values
    m, n = X.shape
    K = initial_centroids.shape[0]
    centroids = initial_centroids
    previous_centroids = centroids    
    idx = np.zeros(m)
    plt.figure(figsize=(8, 6))

    # Run K-Means
    for i in range(max_iters):
        
        #Output progress
        print("K-Means iteration %d/%d" % (i, max_iters-1))
        
        # For each example in X, assign it to the closest centroid
        idx = find_closest_centroids(X, centroids)
        
        # Given the memberships, compute new centroids
        centroids = compute_centroids(X, idx, K)
    plt.show() 
    return centroids, idx

# Set initial centroids
initial_centroids = np.array([[3,3],[6,2],[8,5]])

# Number of iterations
max_iters = 10

# Run K-Means
centroids, idx = run_kMeans(X, initial_centroids, max_iters, plot_progress=True)

print(f"centroids, idx: {centroids},{idx}")



#========================================================================================================================================================================
# Random initialization¶
# The initial assignments of centroids for the example dataset was designed so 
# that you will see the same figure as in Figure 1. In practice, 
# a good strategy for initializing the centroids is to select random examples from the training set.
# In this part of the exercise, you should understand how the function kMeans_init_centroids is implemented.

# The code first randomly shuffles the indices of the examples (using np.random.permutation()).
# Then, it selects the first  𝐾
#   examples based on the random permutation of the indices.
# This allows the examples to be selected at random without the risk of selecting the same example twice.

# You do not need to modify this part

def kMeans_init_centroids(X, K):
    """
    This function initializes K centroids that are to be 
    used in K-Means on the dataset X
    
    Args:
        X (ndarray): Data points 
        K (int):     number of centroids/clusters
    
    Returns:
        centroids (ndarray): Initialized centroids
    """
    # Randomly reorder the indices of examples
    randidx = np.random.permutation(X.shape[0])
    
    # Take the first K examples as centroids
    centroids = X[randidx[:K]]
    
    return centroids

# Set number of centroids and max number of iterations
K = 3
max_iters = 10

# Set initial centroids by picking random examples from the dataset
initial_centroids = kMeans_init_centroids(X, K)

# Run K-Means
centroids, idx = run_kMeans(X, initial_centroids, max_iters, plot_progress=True)