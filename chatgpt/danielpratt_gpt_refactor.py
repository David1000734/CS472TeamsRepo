# Import dataset from ucimlrepo
from ucimlrepo import fetch_ucirepo
park_original = fetch_ucirepo(id=189)

# Fetch input feature and target data then concatenate to make one complete dataset
import pandas as pd
complete = pd.concat([park_original.data.features, park_original.data.targets], axis = 1)

# Removes all non-continuous input features
complete.drop(['age', 'sex'], axis = 'columns', inplace = True)

# Set target and input data
target = complete.total_UPDRS
inputs = complete.drop(['total_UPDRS'], axis = 'columns')

# Splits data into a 80% train/20% test selection for model training
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(inputs, target, test_size = 0.2)



# +---      MODEL GENERATION (SETUP 1)      ---+

# Generate Multi-Layer Perceptron Regressor Model using training data
from sklearn.neural_network import MLPRegressor
model1 = MLPRegressor(max_iter=500).fit(X_train, Y_train)

# Uses model to predict the outcome of the training and testing samples
training1 = model1.predict(X_train)
testing1 = model1.predict(X_test)


# +---      EVALUATION METRICS (SETUP 1)      ---+

# Title and Header
print("+ - - - - - +\nMulti-Layer Perceptron Regressor\n+ - - - - - +\n\n\t(SETUP 1)\n")

#  --- Training Data Metrics ---
print("+-----+ Training Data Metrics +-----+")

# Mean Squared Error
from sklearn.metrics import mean_squared_error
print ("Mean SQUARED Error Of Model \t: " + str(mean_squared_error(Y_train, training1)))

# Mean Absolute  Error
from sklearn.metrics import mean_absolute_error
print ("Mean ABSOLUTE Error Of Model \t: " + str(mean_absolute_error(Y_train, training1)))

# Coefficient of Determination
from sklearn.metrics import r2_score
print ("R2 Of Model \t\t\t: " + str(r2_score(Y_train, training1)))

#  --- Test Data Metrics ---
print("+-----+ Test Data Metrics +-----+")

# Mean Squared Error
print ("Mean SQUARED Error Of Model \t: " + str(mean_squared_error(Y_test, testing1)))

# Mean Absolute  Error
print ("Mean ABSOLUTE Error Of Model \t: " + str(mean_absolute_error(Y_test, testing1)))

# Coefficient of Determination
print ("R2 Of Model \t\t\t: " + str(r2_score(Y_test, testing1)))



# +---      MODEL GENERATION (SETUP 2)      ---+

# Generate Multi-Layer Perceptron Regressor Model using training data
model2 = MLPRegressor(hidden_layer_sizes=(200,), learning_rate='adaptive', max_iter=700).fit(X_train, Y_train)

# Uses model to predict the outcome of the training and testing samples
training2 = model2.predict(X_train)
testing2 = model2.predict(X_test)


# +---      EVALUATION METRICS (SETUP 2)      ---+

# Title and Header
print("\n\n\t(SETUP 2)\n")

#  --- Training Data Metrics ---
print("+-----+ Training Data Metrics +-----+")

# Mean Squared Error
print ("Mean SQUARED Error Of Model \t: " + str(mean_squared_error(Y_train, training2)))

# Mean Absolute  Error
print ("Mean ABSOLUTE Error Of Model \t: " + str(mean_absolute_error(Y_train, training2)))

# Coefficient of Determination
print ("R2 Of Model \t\t\t: " + str(r2_score(Y_train, training2)))

#  --- Test Data Metrics ---
print("+-----+ Test Data Metrics +-----+")

# Mean Squared Error
print ("Mean SQUARED Error Of Model \t: " + str(mean_squared_error(Y_test, testing2)))

# Mean Absolute  Error
print ("Mean ABSOLUTE Error Of Model \t: " + str(mean_absolute_error(Y_test, testing2)))

# Coefficient of Determination
print ("R2 Of Model \t\t\t: " + str(r2_score(Y_test, testing2)))



# +---      MODEL GENERATION (SETUP 3)      ---+

# Generate Multi-Layer Perceptron Regressor Model using training data
model3 = MLPRegressor(hidden_layer_sizes=(150,), activation='logistic', learning_rate='adaptive', max_iter=550).fit(X_train, Y_train)

# Uses model to predict the outcome of the training and testing samples
training3 = model3.predict(X_train)
testing3 = model3.predict(X_test)


# +---      EVALUATION METRICS (SETUP 3)      ---+

# Title and Header
print("\n\n\t(SETUP 3)\n")

#  --- Training Data Metrics ---
print("+-----+ Training Data Metrics +-----+")

# Mean Squared Error
print ("Mean SQUARED Error Of Model \t: " + str(mean_squared_error(Y_train, training3)))

# Mean Absolute  Error
print ("Mean ABSOLUTE Error Of Model \t: " + str(mean_absolute_error(Y_train, training3)))

# Coefficient of Determination
print ("R2 Of Model \t\t\t: " + str(r2_score(Y_train, training3)))

#  --- Test Data Metrics ---
print("+-----+ Test Data Metrics +-----+")

# Mean Squared Error
print ("Mean SQUARED Error Of Model \t: " + str(mean_squared_error(Y_test, testing3)))

# Mean Absolute  Error
print ("Mean ABSOLUTE Error Of Model \t: " + str(mean_absolute_error(Y_test, testing3)))

# Coefficient of Determination
print ("R2 Of Model \t\t\t: " + str(r2_score(Y_test, testing3)))