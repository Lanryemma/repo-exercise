import copy, math
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import SGDRegressor
from sklearn.preprocessing import StandardScaler
# Polynomial Features
# Above we were considering a scenario where the data was non-linear. 
# Let's try using what we know so far to fit a non-linear curve.
# We'll start with a simple quadratic:  𝑦=1+𝑥^2

x = np.arange(0, 20, 1)
print(f"{x}: x.shape = {x.shape}")
# create target data
x = np.arange(0, 20, 1)
y = 1 + x**2

# Engineer features 
X = x**2      #<-- added engineered feature
X = X.reshape(-1, 1)  #X should be a 2-D Matrix
#model_w,model_b = run_gradient_descent_feng(X, y, iterations=10000, alpha = 1e-5)



#======================================================================================================================================
# Linear Regression using Scikit-Learn
# There is an open-source, commercially usable machine learning toolkit called scikit-learn. 
# This toolkit contains implementations of many of the algorithms that you will work with in this course.
X_train, y_train = np.array([[2104, 5, 1, 45], [1416, 3, 2, 40], [852, 2, 1, 35]]), np.array([460, 232, 178])
X_features = ['size(sqft)','bedrooms','floors','age']

#Scale/normalize the training data
scaler = StandardScaler()
X_norm = scaler.fit_transform(X_train)
print(f"Peak to Peak range by column in Raw        X:{np.ptp(X_train,axis=0)}")   
print(f"Peak to Peak range by column in Normalized X:{np.ptp(X_norm,axis=0)}")

#Create and fit the regression model
sgdr = SGDRegressor(max_iter=1000)
sgdr.fit(X_norm, y_train)
print(sgdr)
print(f"number of iterations completed: {sgdr.n_iter_}, number of weight updates: {sgdr.t_}")

#View parameters
# Note, the parameters are associated with the normalized input data. 
# The fit parameters are very close to those found in the previous lab with this data.
b_norm = sgdr.intercept_
w_norm = sgdr.coef_
print(f"model parameters:                   w: {w_norm}, b:{b_norm}")
print( "model parameters from previous lab: w: [110.56 -21.27 -32.71 -37.97], b: 363.16")

#Make predictions
# Predict the targets of the training data. Use both the predict routine and compute using  𝑤
#   and  𝑏.
# make a prediction using sgdr.predict()
y_pred_sgd = sgdr.predict(X_norm)
# make a prediction using w,b. 
y_pred = np.dot(X_norm, w_norm) + b_norm  
print(f"prediction using np.dot() and sgdr.predict match: {(y_pred == y_pred_sgd).all()}")
print(f"Prediction on training set:\n{y_pred[:4]}" )
print(f"Target values \n{y_train[:4]}")


# plot predictions and targets vs original features    
fig,ax=plt.subplots(1,4,figsize=(12,3),sharey=True)
for i in range(len(ax)):
    ax[i].scatter(X_train[:,i],y_train, label = 'target')
    ax[i].set_xlabel(X_features[i])
    ax[i].scatter(X_train[:,i],y_pred,color=["orange"], label = 'predict')
ax[0].set_ylabel("Price"); ax[0].legend();
fig.suptitle("target versus prediction using z-score normalized model")
plt.show()