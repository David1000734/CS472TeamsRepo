# Import dataset from ucimlrepo
from ucimlrepo import fetch_ucirepo
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Fetch data and concatenate input features and target
park_original = fetch_ucirepo(id=189)
complete = pd.concat([park_original.data.features, park_original.data.targets], axis=1)

# Remove non-continuous input features
complete.drop(['age', 'sex'], axis='columns', inplace=True)

# Set target and input data
target = complete.total_UPDRS
inputs = complete.drop(['total_UPDRS'], axis='columns')

# Split data into training and test sets
X_train, X_test, Y_train, Y_test = train_test_split(inputs, target, test_size=0.2)

# Function to train model and display evaluation metrics
def train_and_evaluate(model, X_train, Y_train, X_test, Y_test, setup_name):
    model.fit(X_train, Y_train)
    
    # Predictions
    training_pred = model.predict(X_train)
    testing_pred = model.predict(X_test)

    # Evaluation metrics
    print(f"\n\n+ - - - - - +\nMulti-Layer Perceptron Regressor\n+ - - - - - +\n\n\t({setup_name})\n")
    
    # Training metrics
    print("+-----+ Training Data Metrics +-----+")
    print(f"Mean SQUARED Error Of Model \t: {mean_squared_error(Y_train, training_pred)}")
    print(f"Mean ABSOLUTE Error Of Model \t: {mean_absolute_error(Y_train, training_pred)}")
    print(f"R2 Of Model \t\t\t: {r2_score(Y_train, training_pred)}")
    
    # Test metrics
    print("+-----+ Test Data Metrics +-----+")
    print(f"Mean SQUARED Error Of Model \t: {mean_squared_error(Y_test, testing_pred)}")
    print(f"Mean ABSOLUTE Error Of Model \t: {mean_absolute_error(Y_test, testing_pred)}")
    print(f"R2 Of Model \t\t\t: {r2_score(Y_test, testing_pred)}")

# +--- MODEL GENERATION AND EVALUATION (SETUP 1) ---+
model1 = MLPRegressor(max_iter=500)
train_and_evaluate(model1, X_train, Y_train, X_test, Y_test, 'SETUP 1')

# +--- MODEL GENERATION AND EVALUATION (SETUP 2) ---+
model2 = MLPRegressor(hidden_layer_sizes=(200,), learning_rate='adaptive', max_iter=700)
train_and_evaluate(model2, X_train, Y_train, X_test, Y_test, 'SETUP 2')

# +--- MODEL GENERATION AND EVALUATION (SETUP 3) ---+
model3 = MLPRegressor(hidden_layer_sizes=(150,), activation='logistic', learning_rate='adaptive', max_iter=550)
train_and_evaluate(model3, X_train, Y_train, X_test, Y_test, 'SETUP 3')
