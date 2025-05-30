# Import modules and packages
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt


# Functions and procedures
def plot_predictions(train_data, train_labels,  test_data, test_labels,  predictions):
  """
  Plots training data, test data and compares predictions.
  """
  plt.figure(figsize=(6, 5))
  # Plot training data in blue
  plt.scatter(train_data, train_labels, c="b", label="Training data")
  # Plot test data in green
  plt.scatter(test_data, test_labels, c="g", label="Testing data")
  # Plot the predictions in red (predictions were made on the test data)
  plt.scatter(test_data, predictions, c="r", label="Predictions")
  # Show the legend
  plt.legend(shadow=True)
  # Set grids
  plt.grid(which='major', c='#cccccc', linestyle='--', alpha=0.5)
  # Some text
  plt.title('Model Results', family='DejaVu Sans', fontsize=14)
  plt.xlabel('X axis values', family='DejaVu Sans', fontsize=11)
  plt.ylabel('Y axis values', family='DejaVu Sans', fontsize=11)
  # Show
  plt.savefig('model_results.png', dpi=120)



def mae(y_test, y_pred):
  """
  Calculuates mean absolute error between y_test and y_preds.
  """
  return tf.metrics.mean_absolute_error(y_test, y_pred)
  

def mse(y_test, y_pred):
  """
  Calculates mean squared error between y_test and y_preds.
  """
  return tf.metrics.mean_squared_error(y_test, y_pred)


# Check Tensorflow version
print(tf._version_)


# Create features
X = np.arange(-100, 100, 4)

# Create labels
y = np.arange(-90, 110, 4)


# Split data into train and test sets
X_train = X[:40] # first 40 examples (80% of data)
y_train = y[:40]

X_test = X[40:] # last 10 examples (20% of data)
y_test = y[40:]


# Take a single example of X
# Reshape inputs to 2D
X_train = X_train.reshape(-1, 1)
X_test = X_test.reshape(-1, 1)

# Input shape
input_shape = X_train[0].shape

# Create a model using the Sequential API
# Create a model using the Sequential API
model = tf.keras.Sequential([
    tf.keras.layers.Dense(1, input_shape=input_shape)
])

# Compile and train
model.compile(loss='mae',
              optimizer=tf.keras.optimizers.SGD(),
              metrics=['mae'])

model.fit(X_train, y_train, epochs=100)

# Make and plot predictions for model_1
y_preds = model.predict(X_test)
plot_predictions(train_data=X_train, train_labels=y_train,  test_data=X_test, test_labels=y_test,  predictions=y_preds)

# Fix MAE and MSE calculations
from tensorflow.keras import backend as K

def mae(y_test, y_pred):
    return K.mean(K.abs(y_test - y_pred))

def mse(y_test, y_pred):
    return K.mean(K.square(y_test - y_pred))

# Calculate model_1 metrics
mae_1 = np.round(float(mae(y_test, y_preds.squeeze()).numpy()), 2)
mse_1 = np.round(float(mse(y_test, y_preds.squeeze()).numpy()), 2)
print(f'\nMean Absolute Error = {mae_1}, Mean Squared Error = {mse_1}.')

# Write metrics to file
with open('metrics.txt', 'w') as outfile:
    outfile.write(f'\nMean Absolute Error = {mae_1}, Mean Squared Error = {mse_1}.')
