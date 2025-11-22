import numpy as np
import matplotlib.pyplot as plt


# You will use X_train to fit a Gaussian distribution
# You will use X_val and y_val as a cross validation set to select a threshold and determine anomalous vs normal examples
X_train = np.array([[13.04681517, 14.74115241],
 [13.40852019, 13.7632696 ],
 [14.19591481, 15.85318113],
 [14.91470077, 16.17425987],
 [13.57669961, 14.04284944],
 [13.92240251, 13.40646894],
 [12.82213164, 14.22318782],
 [15.67636615 ,15.89169137],
 [16.16287532 ,16.20299807],
 [12.66645095 ,14.89908374],
 [13.98454962, 12.95800822],
 [14.06146043 ,14.54908874],
 [13.38988671, 15.56202142],
 [13.39350475, 15.62698794],
 [13.97900926, 13.28061494],
 [14.16791259, 14.46583829],
 [13.96176145, 14.75182421],
 [14.45899735, 15.07018563],
 [14.58476372, 15.82743424],
 [12.07427074, 13.0671109 ],
 [13.5491294,  15.53827677],
 [13.98625042, 14.78776304],
 [14.96991942, 16.51830493],
 [14.25576597, 15.29427277],
 [15.33425,    16.12469989],
 [15.6350487,  16.49094477],
 [13.62081292, 15.45947525],
 [14.81548485, 15.33956527],
 [14.59318973, 14.61238106],
 [14.48906755, 15.64087368],
 [15.52704801, 14.63568031],
 [13.97506707, 14.76531533],
 [12.95364954, 14.82328512],
 [12.88787444, 15.0760781 ],
 [16.02178961, 16.25746992],
 [14.92629271, 16.29725072],
 [12.465594,   14.18321212],
 [14.08466278, 14.44192203],
 [14.53717523, 14.24224248],
 [14.22250852, 15.42386188],
 [14.51908496, 13.99871699],
 [13.11971434, 14.66081846],
 [14.51088894, 15.30465149],
 [14.18262426, 15.39388968],
 [14.71651845, 15.73369667],
 [13.834547  , 16.17138034],
 [16.00076179, 14.6923297 ],
 [14.12702715, 15.91462775],
 [13.84578547, 14.34139349],
 [15.4142611 , 16.24243182],
 [13.25273727, 15.00861364],
 [13.66840226, 14.35886036],
 [13.77534774, 14.73808512],
 [14.12582343, 14.92980923],
 [14.54724604, 15.63339445],
 [14.15258077, 14.53622697],
 [14.12648161, 15.34467591],
 [14.26324658, 14.98556918],
 [14.77324332, 15.25299474],
 [14.20969934, 16.14572569],
 [13.26065515, 15.48016214],
 [14.25273351, 15.03134361],
 [12.92124447, 13.1932154 ],
 [13.85243129, 13.33213111],
 [13.968568,   13.19821237],
 [13.25206982, 15.3684639 ],
 [13.70449634, 13.21431302],
 [14.50874721, 15.46051652],
 [15.69042696, 16.48168852],
 [12.95598192, 12.43703006],
 [13.59312604, 14.84189903],
 [15.12874639, 17.14981223],
 [14.26705037, 15.67551974],
 [15.66145055, 14.81146451],
 [14.33962673, 15.49202298],
 [14.27617655, 14.70590693],
 [14.86049072, 15.59000779],
 [14.1041448,  15.18050456],
 [15.98828286, 15.62105187],
 [13.47473583, 15.59307142],
 [13.77637601, 14.99194427],
 [12.82770875, 15.67136907],
 [13.67165486, 15.11954159],
 [15.38704284, 15.56936935],
 [15.54320934, 15.5154315 ],
 [13.85306094, 15.60672437],
 [13.62525246, 14.45209463],
 [15.01577844, 14.91664093],
 [13.83645753, 15.24940725],
 [14.22694439, 14.34798436],
 [13.23742625, 14.61058751],
 [13.38482919, 14.7331933 ],
 [13.87130103, 14.97399469],
 [12.39445847, 14.64448217],
 [14.32186558, 14.52890629],
 [15.82965092, 15.71619455],
 [15.80177302, 16.01808914],
 [14.697512  , 14.11198749],
 [14.70598657, 16.46040295],
 [13.5915686,  14.91975097]])


X_val= np.array([[15.79025979, 14.9210243 ],
 [13.63961877, 15.32995521],
 [14.86589943, 16.47386514],
 [13.58467605 ,13.98930611],
 [13.46404167, 15.63533011],
 [12.94888838 ,16.14006828],
 [15.31084155, 15.17480137],
 [13.89795241 ,15.43169469],
 [11.92096525 ,14.30579937],
 [14.85934119, 14.90066474],
 [13.63501268 ,14.5620583 ],
 [15.75981741, 15.13340409],
 [15.221965 ,  14.18491044],
 [12.10564111, 13.42653822],
 [14.80848889, 13.87075725],
 [15.36135887, 15.99014917],
 [12.72914442, 15.8265107 ],
 [15.38533789, 15.21036416],
 [13.81810534, 14.29933915],
 [15.3788488 , 15.90228514],
 [14.11232153, 15.31616729],
 [12.82415241, 13.6971992 ],
 [14.58354683, 14.99675181],
 [14.2948367,  15.84651796],
 [13.5112881 , 15.5909427 ],
 [13.71433284, 15.35484382],
 [12.85788467, 14.00239134],
 [14.56998008 ,14.22432035],
 [15.59049569, 15.72143533],
 [13.0999943,  15.0900635 ],
 [14.61461465, 14.85494525],
 [13.92751557, 16.09420913],
 [13.28968651, 15.42177935],
 [14.3283751,  15.01104801],
 [12.99369072, 15.02922303],
 [13.21733162, 15.02076411],
 [13.72874052, 14.03641262],
 [12.59667946, 13.4656785 ],
 [14.03082134, 16.31086646],
 [14.06074927, 15.32971274],
 [15.26965979, 15.57677091],
 [15.88197423, 15.46171487],
 [15.07180425, 14.41570779],
 [13.98475169, 15.47191457],
 [14.16180226, 14.81511294],
 [14.68681165, 14.4135602 ],
 [14.11912326, 16.76631594],
 [14.31950715, 15.38060917],
 [13.30913392, 15.04326285],
 [13.55172581, 14.01841776]])

Y_val =np.array([0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0, 1 ,0, 0, 0 ,0 ,0, 0 ,0 ,0, 0 ,0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0, 0, 0 ,0,
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])

# To perform anomaly detection, you will first need to fit a model to the data’s distribution.
# Given a training set {x(1),...,x(m)} you want to estimate the Gaussian distribution for each of the features xi.
#p(x,mu,va**2) = (1/((2*Pi*(var**2))**(1/2)))np.exp(-(((x-mu)**2)/2*var**2)

#where μ(mu) is the mean and σ(var) is the variance
#the estimate_gaussian function below to calculate 
# mu (mean for each feature in X) and var (variance for each feature in X).
# UNQ_C1
# GRADED FUNCTION: estimate_gaussian

def estimate_gaussian(X): 
    """
    Calculates mean and variance of all features 
    in the dataset
    
    Args:
        X (ndarray): (m, n) Data matrix
    
    Returns:
        mu (ndarray): (n,) Mean of all features
        var (ndarray): (n,) Variance of all features
    """
#     axis=0 → (sum of each column)
#     axis=1 → (sum of each row)
    m, n = X.shape
    
    ### START CODE HERE ### 
    #You can use np.sum to with `axis = 0` parameter to get the sum for each column of an array
    mu = (1 / m) * np.sum(X, axis = 0)
    
#     You can use np.sum to with `axis = 0` parameter to get the 
#     sum for each column of an array and **2 to get the square.
    
    var = (1 / m) * np.sum((X - mu) ** 2, axis = 0)
    
    ### END CODE HERE ### 
        
    return mu, var

# Estimate mean and variance of each feature
mu, var = estimate_gaussian(X_train)              
print("Mean of each feature:", mu)
print("Variance of each feature:", var)

#tp get the probability of it being an anomaly
def multivariate_gaussian(X_val, mu, var):
    #     axis=0 → (sum of each column)
    #     axis=1 → (sum of each row)
    Xv = X_val
    # m, n = Xv.shape
    # Pi = 3.142
    # p_val = (1/((2*Pi*(var**2))**(1/2)))*np.exp(-(np.sum((Xv - mu) ** 2, axis = 0)/2*var**2))
    n = len(mu)
    p_val = np.ones(Xv.shape[0])
    
    for j in range(n):
        p_val = p_val * (1 / np.sqrt(2 * np.pi * var[j])) * np.exp(-(Xv[:, j] - mu[j]) ** 2 / (2 * var[j]))
    
    return p_val
# the select_threshold function below to find the best threshold to use for selecting outliers based 
# on the results from the validation set (p_val) and the ground truth (y_val).
#Recall that if an example  𝑥 has a low probability  𝑝(𝑥)<𝜀, then it is classified as an anomaly
#we are to select the best  𝜀 based on the  𝐹1 score.
# recall that precision(prec) = tp/(tp+fp)
#------------ recall (rec) = tp/(tp+fn)
# where
# 𝑡𝑝 is the number of true positives: the ground truth label says 
#   it’s an anomaly and our algorithm correctly classified it as an anomaly.
# 𝑓𝑝 is the number of false positives: the ground truth label says 
#   it’s not an anomaly, but our algorithm incorrectly classified it as an anomaly.
# 𝑓𝑛 is the number of false negatives: the ground truth label says 
#   it’s an anomaly, but our algorithm incorrectly classified it as not being anomalous.
# 𝐹1 score = 2*prec*rec/(prec + rec)
def select_threshold(y_val, p_val): 
    """
    Finds the best threshold to use for selecting outliers 
    based on the results from a validation set (p_val) 
    and the ground truth (y_val)
    
    Args:
        y_val (ndarray): Ground truth on validation set
        p_val (ndarray): Results on validation set
        
    Returns:
        epsilon (float): Threshold chosen 
        F1 (float):      F1 score by choosing epsilon as threshold
    """ 

    best_epsilon = 0
    best_F1 = 0
    F1 = 0
    
    step_size = (max(p_val) - min(p_val)) / 1000
    
    for epsilon in np.arange(min(p_val), max(p_val), step_size):
    
        ### START CODE HERE ### 
        prediction = (p_val < epsilon)
        tp = sum((prediction == 1) & (y_val == 1))
        fp = sum((prediction == 1) & (y_val == 0))
        fn = sum((prediction == 0) & (y_val == 1))
        prec = tp/(tp + fp)
        rec = tp/(tp + fn)
        F1= (2*prec*rec)/(prec + rec)
        
        ### END CODE HERE ### 
        
        if F1 > best_F1:
            best_F1 = F1
            best_epsilon = epsilon
        
    return best_epsilon, best_F1

p_val = multivariate_gaussian(X_val, mu, var)
epsilon, F1 = select_threshold(Y_val, p_val)
print('Best epsilon found using cross-validation: %e' % epsilon)
print('Best F1 on Cross Validation Set: %f' % F1)
print('# Anomalies found: %d'% sum(p_val < epsilon))