import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
import matplotlib.pyplot as plt
#import (heart.csv)


#Cardiovascular disease (CVDs) is the number one cause of death globally, 
# taking an estimated 17.9 million lives each year, which accounts for 31% of all deaths worldwide. 
# Four out of five CVD deaths are due to heart attacks and strokes, and one-third of these deaths occur 
# prematurely in people under 70 years of age. Heart failure is a common event caused by CVDs.

# Let's now load the dataset. As we can see above, the variables:

# Sex
# ChestPainType
# RestingECG
# ExerciseAngina
# ST_Slope
#===================================================================================================
# the full categorical include Age,Sex,	ChestPainType,	RestingBP,	Cholesterol, FastingBS,
# RestingECG,	MaxHR,	ExerciseAngina,	Oldpeak	ST_Slope,	HeartDisease, 
# so we must one-hot encode them.
# Load the dataset using pandas
df = pd.read_csv("C:\\Users\\user\\Documents\\LANRE\\Desktop\\FRONTEND\\Machine_Learning\\heart.csv")
print(df.head())

# One-hot encoding using Pandas
# First we will remove the binary variables, because one-hot encoding them would do nothing to them.
# To achieve this we will just count how many different values there are in each categorical variable 
# and consider only the variables with 3 or more values.
cat_variables = ['Sex',
'ChestPainType',
'RestingECG',
'ExerciseAngina',
'ST_Slope'
]

#  one-hot encoding aims to transform a categorical variable with n outputs into n binary variables.
# Pandas has a built-in method to one-hot encode variables, 
# it is the function pd.get_dummies. There are several arguments to this function, 
# but here we will use only a few. They are:
# data: DataFrame to be used
# prefix: A list with prefixes, so we know which value we are dealing with
# columns: the list of columns that will be one-hot encoded. 'prefix' and 'columns' must have the same length.

# This will replace the columns with the one-hot encoded ones and keep the columns outside 'columns' argument as it is.
df = pd.get_dummies(data = df,
                        prefix = cat_variables,
                        columns = cat_variables)

print(df.head())

# let's choose the variables that will be the input features of the model.
# The target is HeartDisease.
features = [x for x in df.columns if x not in 'HeartDisease'] ## Removing our target variable
#We started with 11 features. Let's see how many feature variables we have after one-hot encoding.
print(len(features))


#we will split our dataset into train and test datasets. We will use the function train_test_split from Scikit-learn.
X_train, X_val, y_train, y_val = train_test_split(df[features], df['HeartDisease'],
                                                train_size = 0.8, random_state = 42)

# We will keep the shuffle = True since our dataset has not any time dependency.
print(f'train samples: {len(X_train)}')
print(f'validation samples: {len(X_val)}')
print(f'target proportion: {sum(y_train)/len(y_train):.4f}')

# Decision Tree
# In this section, let's work with the Decision Tree we previously learned, 
# but now using the Scikit-learn implementation.

# The hyperparameters we will use and investigate here are:

# min_samples_split: The minimum number of samples required to split an internal node.
# Choosing a higher min_samples_split can reduce the number of splits and may help to reduce overfitting.
# max_depth: The maximum depth of the tree.
# Choosing a lower max_depth can reduce the number of splits and may help to reduce overfitting.

min_samples_split_list = [2,10, 30, 50, 100, 200, 300, 700] ## If the number is an integer, 
#then it is the actual quantity of samples,
max_depth_list = [1,2, 3, 4, 8, 16, 32, 64, None] # None means that there is no depth limit.

accuracy_list_train = []
accuracy_list_val = []
for min_samples_split in min_samples_split_list:
    # You can fit the model at the same time you define it, because the fit function returns the fitted estimator.
    model = DecisionTreeClassifier(min_samples_split = min_samples_split,
                                random_state = 42).fit(X_train,y_train) 
    predictions_train = model.predict(X_train) ## The predicted values for the train dataset
    predictions_val = model.predict(X_val) ## The predicted values for the test dataset
    accuracy_train = accuracy_score(predictions_train,y_train)
    accuracy_val = accuracy_score(predictions_val,y_val)
    accuracy_list_train.append(accuracy_train)
    accuracy_list_val.append(accuracy_val)

#Note how increasing the the number of min_samples_split reduces overfitting.
#ncreasing min_samples_split from 10 to 30, and from 30 to 50  improve the validation accuracy

#Let's do the same experiment with max_depth
accuracy_list_train = []
accuracy_list_val = []
for max_depth in max_depth_list:
    # You can fit the model at the same time you define it, because the fit function returns the fitted estimator.
    model = DecisionTreeClassifier(max_depth = max_depth,
                                random_state = 42).fit(X_train,y_train) 
    predictions_train = model.predict(X_train) ## The predicted values for the train dataset
    predictions_val = model.predict(X_val) ## The predicted values for the test dataset
    accuracy_train = accuracy_score(predictions_train,y_train)
    accuracy_val = accuracy_score(predictions_val,y_val)
    accuracy_list_train.append(accuracy_train)
    accuracy_list_val.append(accuracy_val)

plt.title('Train x Validation metrics')
plt.xlabel('max_depth')
plt.ylabel('accuracy')
plt.xticks(ticks = range(len(max_depth_list )),labels=max_depth_list)
plt.plot(accuracy_list_train)
plt.plot(accuracy_list_val)
plt.legend(['Train','Validation'])
plt.show()


# We can see that in general, reducing max_depth can help to reduce overfitting.
# Reducing max_depth from 8 to 4 increases validation accuracy closer 
# to training accuracy, while significantly reducing training accuracy.
# The validation accuracy reaches the highest at tree_depth=4.

#So we can choose the best values for these two hyper-parameters for our model to be:
max_depth = 4
min_samples_split = 50

decision_tree_model = DecisionTreeClassifier(min_samples_split = 50,
                                            max_depth = 3,
                                            random_state = 42).fit(X_train,y_train)
print(f"Metrics train:\n\tAccuracy score: {accuracy_score(decision_tree_model.predict(X_train),y_train):.4f}")
print(f"Metrics validation:\n\tAccuracy score: {accuracy_score(decision_tree_model.predict(X_val),y_val):.4f}")

#===========================================================================================================================
#for Random Forest algorithm also, using the Scikit-learn implementation.
n_estimators_list = [10,50,100,500]
#we use One additional hyperparameter for Random Forest is called n_estimators 
# which is the number of Decision Trees that make up the Random Forest.

#we use  model = RandomForestClassifier(max_depth = max_depth,
#                                   random_state = RANDOM_STATE).fit(X_train,y_train) 
#for for max_depth and max_depth_list

accuracy_list_train = []
accuracy_list_val = []
for n_estimators in n_estimators_list:
    # You can fit the model at the same time you define it, because the fit function returns the fitted estimator.
    model = RandomForestClassifier(n_estimators = n_estimators,
                                random_state = 42).fit(X_train,y_train) 
    predictions_train = model.predict(X_train) ## The predicted values for the train dataset
    predictions_val = model.predict(X_val) ## The predicted values for the test dataset
    accuracy_train = accuracy_score(predictions_train,y_train)
    accuracy_val = accuracy_score(predictions_val,y_val)
    accuracy_list_train.append(accuracy_train)
    accuracy_list_val.append(accuracy_val)

plt.title('Train x Validation metrics')
plt.xlabel('n_estimators')
plt.ylabel('accuracy')
plt.xticks(ticks = range(len(n_estimators_list )),labels=n_estimators_list)
plt.plot(accuracy_list_train)
plt.plot(accuracy_list_val)
plt.legend(['Train','Validation'])
plt.show()

#Let's then fit a random forest with the following parameters:

max_depth: 16
min_samples_split: 10
n_estimators: 100

random_forest_model = RandomForestClassifier(n_estimators = 100,
                                            max_depth = 16, 
                                            min_samples_split = 10).fit(X_train,y_train)


#==================================================================================================
# XGBoost
# Next is the Gradient Boosting model, called XGBoost. 
# The boosting methods train several trees, but instead of them being uncorrelated to each other,
# now the trees are fit one after the other in order to minimize the error.
#First, let's define a subset of our training set (we should not use the test set here).
n = int(len(X_train)*0.8) ## Let's use 80% to train and 20% to eval
X_train_fit, X_train_eval, y_train_fit, y_train_eval = X_train[:n], X_train[n:], y_train[:n], y_train[n:]

xgb_model = XGBClassifier(n_estimators = 500, learning_rate = 0.1,verbosity = 1, random_state = 42)
xgb_model.fit(X_train_fit,y_train_fit, eval_set = [(X_train_eval,y_train_eval)], early_stopping_rounds = 10)

# Even though we initialized the model to allow up to 500 estimators, 
# the algorithm only fit 26 estimators (over 26 rounds of training).
# To see why, let's look for the round of training that had the best 
# performance (lowest evaluation metric). 
# You can either view the validation log loss metrics that were output above, 
# or view the model's .best_iteration attribute:

print(xgb_model.best_iteration)

# The best round of training was round 16, with a log loss of 4.3948.
# For 10 rounds of training after that (from round 17 to 26), the log loss was higher than this.
print(f"Metrics train:\n\tAccuracy score: {accuracy_score(xgb_model.predict(X_train),y_train):.4f}\nMetrics test:\n\tAccuracy score: {accuracy_score(xgb_model.predict(X_val),y_val):.4f}")

print(f"Metrics train:\n\tAccuracy score: {accuracy_score(xgb_model.predict(X_train),y_train):.4f}\nMetrics test:\n\tAccuracy score: {accuracy_score(xgb_model.predict(X_val),y_val):.4f}")
# Metrics train:
# 	Accuracy score: 0.9251
# Metrics test:
# 	Accuracy score: 0.8641