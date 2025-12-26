import numpy as np
import numpy.ma as ma
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split

# Content-based filtering also generates a user and movie feature vector but recognizes there may be other 
# information available about the user and/or movie that may improve the prediction.
# There are 14 genres. The engineered feature is an average rating derived from the user ratings.
# The user content is composed of engineered features. A per genre average rating is computed per user.
# Additionally, a user id, rating count and rating average are available but not included in 
# the training or prediction content. 
# They are carried with the data set because they are useful in interpreting data.

# Load Data, set configuration variables
item_train, user_train, y_train, item_features, user_features, item_vecs, movie_dict, user_to_genre = load_data()

num_user_features = user_train.shape[1] - 3  # remove userid, rating count and ave rating during training
num_item_features = item_train.shape[1] - 1  # remove movie id at train time
uvs = 3  # user genre vector start
ivs = 3  # item genre vector start
u_s = 3  # start of columns to use in training, user
i_s = 1  # start of columns to use in training, items
#Some of the user and item/movie features are not used in training.
#for user genre, column (0,1 and 2) are not used because u_s = 3
#for item/movie, column(0) is not used because i_s = 1


#Preparing the training data
# Recall in Course 1, Week 2, you explored feature scaling as a means of improving convergence. 
# We'll scale the input features using the scikit learn StandardScaler
#We'll scale the target ratings using a Min Max Scaler which scales the target to be between -1 and 1
# scale training data
item_train_unscaled = item_train
user_train_unscaled = user_train
y_train_unscaled    = y_train

scalerItem = StandardScaler()
scalerItem.fit(item_train)
item_train = scalerItem.transform(item_train)

scalerUser = StandardScaler()
scalerUser.fit(user_train)
user_train = scalerUser.transform(user_train)

scalerTarget = MinMaxScaler((-1, 1))
scalerTarget.fit(y_train.reshape(-1, 1))
y_train = scalerTarget.transform(y_train.reshape(-1, 1))
#ynorm_test = scalerTarget.transform(y_test.reshape(-1, 1))

print(np.allclose(item_train_unscaled, scalerItem.inverse_transform(item_train)))
print(np.allclose(user_train_unscaled, scalerUser.inverse_transform(user_train)))

#==========================================================================================================================
# To allow us to evaluate the results, we will split the data into training and 
# test sets as was discussed in Course 2, Week 3. 
# Here we will use sklean train_test_split to split and shuffle the data.
item_train, item_test = train_test_split(item_train, train_size=0.80, shuffle=True, random_state=1)
user_train, user_test = train_test_split(user_train, train_size=0.80, shuffle=True, random_state=1)
y_train, y_test       = train_test_split(y_train,    train_size=0.80, shuffle=True, random_state=1)
print(f"movie/item training data shape: {item_train.shape}")
print(f"movie/item test data shape: {item_test.shape}")


#==================================================================================================================================
# Neural Network for content-based filtering
# Now, let's construct a neural network as described in the figure above. 
# It will have two networks that are combined by a dot product. You will construct the two networks. 
# In this example, they will be identical. Note that these networks do not need to be the same.

# Use a Keras sequential model
# The first layer is a dense layer with 256 units and a relu activation.
# The second layer is a dense layer with 128 units and a relu activation.
# The third layer is a dense layer with num_outputs units and a linear or no activation.
# GRADED_CELL
# UNQ_C1

num_outputs = 32
tf.random.set_seed(1)
user_NN = tf.keras.models.Sequential([
    ### START CODE HERE ###     
    tf.keras.layers.Dense(256, activation = 'relu'),
    tf.keras.layers.Dense(128, activation = 'relu'),
    tf.keras.layers.Dense(num_outputs, activation ='linear')
    ### END CODE HERE ###  
])

item_NN = tf.keras.models.Sequential([
    ### START CODE HERE ###     
    tf.keras.layers.Dense(256, activation = 'relu'),
    tf.keras.layers.Dense(128, activation = 'relu'),
    tf.keras.layers.Dense(num_outputs, activation ='linear')
    ### END CODE HERE ###  
])

# create the user input and point to the base network
input_user = tf.keras.layers.Input(shape=(num_user_features))
vu = user_NN(input_user)
vu = tf.linalg.l2_normalize(vu, axis=1)

# create the item input and point to the base network
input_item = tf.keras.layers.Input(shape=(num_item_features))
vm = item_NN(input_item)
vm = tf.linalg.l2_normalize(vm, axis=1)

# compute the dot product of the two vectors vu and vm
output = tf.keras.layers.Dot(axes=1)([vu, vm])

# specify the inputs and output of the model
model = tf.keras.Model([input_user, input_item], output)

model.summary()


#=============================================================================================================================
#We will use a mean squared error loss and an Adam optimizer to find the loss function.
tf.random.set_seed(1)
cost_fn = tf.keras.losses.MeanSquaredError()
opt = keras.optimizers.Adam(learning_rate=0.01)
model.compile(optimizer=opt,
            loss=cost_fn)

tf.random.set_seed(1)
model.fit([user_train[:, u_s:], item_train[:, i_s:]], y_train, epochs=30)


#==================================================================================================================================
#Predictions
#Below, you'll use your model to make predictions in a number of circumstances
# Predictions for a new user
# First, we'll create a new user and have the model suggest movies for that user. 
# After you have tried this on the example user content
new_user_id = 5000
new_rating_ave = 0.0
new_action = 0.0
new_adventure = 5.0
new_animation = 0.0
new_childrens = 0.0
new_comedy = 0.0
new_crime = 0.0
new_documentary = 0.0
new_drama = 0.0
new_fantasy = 5.0
new_horror = 0.0
new_mystery = 0.0
new_romance = 0.0
new_scifi = 0.0
new_thriller = 0.0
new_rating_count = 3

user_vec = np.array([[new_user_id, new_rating_count, new_rating_ave,
                    new_action, new_adventure, new_animation, new_childrens,
                    new_comedy, new_crime, new_documentary,
                    new_drama, new_fantasy, new_horror, new_mystery,
                    new_romance, new_scifi, new_thriller]])

# The new user enjoys movies from the adventure, fantasy genres. Let's find the top-rated movies for the new user.
# Below, we'll use a set of movie/item vectors, item_vecs that have a vector for each movie in the training/test set. 
# This is matched with the new user vector above and the scaled vectors are used to predict ratings for all the movies.
# generate and replicate the user vector to match the number movies in the data set.
user_vecs = gen_user_vecs(user_vec,len(item_vecs))

# scale our user and item vectors
suser_vecs = scalerUser.transform(user_vecs)
sitem_vecs = scalerItem.transform(item_vecs)

# make a prediction
y_p = model.predict([suser_vecs[:, u_s:], sitem_vecs[:, i_s:]])

# unscale y prediction 
y_pu = scalerTarget.inverse_transform(y_p)

# sort the results, highest prediction first
sorted_index = np.argsort(-y_pu,axis=0).reshape(-1).tolist()  #negate to get largest rating first
sorted_ypu   = y_pu[sorted_index]
sorted_items = item_vecs[sorted_index]  #using unscaled vectors for display

print_pred_movies(sorted_ypu, sorted_items, movie_dict, maxcount = 10)


#=============================================================================================================================
# Finding Similar Items¶
# The neural network above produces two feature vectors, a user feature vector  𝑣𝑢
# , and a movie feature vector,  𝑣𝑚
# . These are 32 entry vectors whose values are difficult to interpret. However, 
# similar items will have similar vectors. This information can be used to make recommendations. 
# For example, if a user has rated "Toy Story 3" highly,
# one could recommend similar movies by selecting movies with similar movie feature vectors.
#A similarity measure is the squared distance between the two vectors 𝐯(𝐤)𝐦 and 𝐯(𝐢)𝐦
#:‖‖V(𝐤)𝐦−V(𝐢)𝐦‖‖**2
def sq_dist(a,b):
    """
    Returns the squared distance between two vectors
    Args:
      a (ndarray (n,)): vector with n features
      b (ndarray (n,)): vector with n features
    Returns:
      d (float) : distance
    """
    ### START CODE HERE ###     
    d = np.sum(np.square(a - b))
    ### END CODE HERE ###     
    return d

# to test our function
a1 = np.array([1.0, 2.0, 3.0]); b1 = np.array([1.0, 2.0, 3.0])
a2 = np.array([1.1, 2.1, 3.1]); b2 = np.array([1.0, 2.0, 3.0])
a3 = np.array([0, 1, 0]);       b3 = np.array([1, 0, 0])
print(f"squared distance between a1 and b1: {sq_dist(a1, b1):0.3f}")
print(f"squared distance between a2 and b2: {sq_dist(a2, b2):0.3f}")
print(f"squared distance between a3 and b3: {sq_dist(a3, b3):0.3f}")

#A matrix of distances between movies can be computed once when the model is trained and 
# sthen reused for new recommendations without retraining.
#we will use the trained item_NN and build a small model to allow us to run the movie vectors through it to generate  𝑣𝑚
input_item_m = tf.keras.layers.Input(shape=(num_item_features))    # input layer
vm_m = item_NN(input_item_m)                                       # use the trained item_NN
vm_m = tf.linalg.l2_normalize(vm_m, axis=1)                        # incorporate normalization as was done in the original model
model_m = tf.keras.Model(input_item_m, vm_m)                                
model_m.summary()

#Once you have a movie model, you can create a set of movie feature vectors by using 
# the model to predict using a set of item/movie vectors as input. 
# `item_vecs` is a set of all of the movie vectors.
#It must be scaled to use with the trained model. 
# The result of the prediction is a 32 entry feature vector for each movie.
scaled_item_vecs = scalerItem.transform(item_vecs)
vms = model_m.predict(scaled_item_vecs[:,i_s:])
print(f"size of all predicted movie feature vectors: {vms.shape}")

#We can then find the closest movie by finding the minimum along each row. 
# We will make use of numpy masked arrays to avoid selecting the same movie

count = 50  # number of movies to display
dim = len(vms)
dist = np.zeros((dim,dim))

for i in range(dim):
    for j in range(dim):
        dist[i,j] = sq_dist(vms[i, :], vms[j, :])
        
m_dist = ma.masked_array(dist, mask=np.identity(dist.shape[0]))  # mask the diagonal

disp = [["movie1", "genres", "movie2", "genres"]]
for i in range(count):
    min_idx = np.argmin(m_dist[i])
    movie1_id = int(item_vecs[i,0])
    movie2_id = int(item_vecs[min_idx,0])
    disp.append( [movie_dict[movie1_id]['title'], movie_dict[movie1_id]['genres'],
                  movie_dict[movie2_id]['title'], movie_dict[movie1_id]['genres']]
               )
table = tabulate.tabulate(disp, tablefmt='html', headers="firstrow")
table