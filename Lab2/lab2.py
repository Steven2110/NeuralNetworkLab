# -*- coding: utf-8 -*-
"""Lab2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lVtJNEbM0ouLjciwJ9j6P7BMnrzg1JGz
"""

from google.colab import drive
drive.mount('/content/gdrive')

import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.layers import Dropout
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

file_name = "/content/gdrive/MyDrive/TSU/Lab_Neural_Network/Lab2/Khabarovsk_weather.csv"

df = pd.read_csv(file_name, sep=';')
df.head(10)

df.drop('DD', axis=1, inplace=True)
df.head(10)

df.describe()

df.info()

df.hist()

df = df[['LocalTime','T']]
df.head()

df.isna().sum()

df.dropna(inplace=True)

df.isna().sum()

plt.plot(range(1,len(df['T'].values)+1),df['T'].values)

# Extract and normalize the target column
min_max_scaler = MinMaxScaler()
df = df['T'].values
df = min_max_scaler.fit_transform(df.reshape(-1, 1))

df.shape

# Flatten the data shape
df = df.flatten()
df.shape

"""## Split data to train, test, and validation"""

window = 15

# Calculate the number of samples for training, validation, and test sets
n_samples = df.shape[0] - window
n_train_samples = round(0.7 * n_samples)
n_val_samples = round(0.15 * n_samples)
n_test_samples = n_samples - n_train_samples - n_val_samples

print('Train = ',n_train_samples,'Validation = ',n_val_samples,'Test = ',n_test_samples)

# Function to create input-output pairs for a given set
def create_pairs(start_index, num_samples):
    X = [df[start_index + i : start_index + i + window] for i in range(num_samples)]
    y = [df[start_index + i + window] for i in range(num_samples)]
    return np.array(X), np.array(y)

# Create training, validation, and test sets
X_train, y_train = create_pairs(0, n_train_samples)
X_val, y_val = create_pairs(n_train_samples, n_val_samples)
X_test, y_test = create_pairs(n_train_samples + n_val_samples, n_test_samples)

# Reshape the data
X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
X_val = np.reshape(X_val, (X_val.shape[0], 1, X_val.shape[1]))
X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

"""# Regressor (RNN)"""

# Build the RNN model
rnn_model = tf.keras.Sequential([
    tf.keras.layers.SimpleRNN(10, activation='sigmoid', input_shape=(X_train.shape[1], X_train.shape[2])),
    Dropout(0.2),
    tf.keras.layers.Dense(1, activation='linear')
])

# Compile the RNN model
rnn_model.compile(loss='mse',
                  optimizer='adam',
                  metrics='mae')

# Train the RNN model
rnn_history = rnn_model.fit(
    X_train,
    y_train,
    epochs=10,
    batch_size=20,
    validation_data=(X_val, y_val)
)

"""## MSE, MAE R2"""

# Get R2, MSE, & MAE scores
y_pred = rnn_model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)

mae = mean_absolute_error(y_test, y_pred)

r2 = r2_score(y_test, y_pred)

print(f"MSE: {mse:.2f}")
print(f"MAE: {mae:.2f}")
print(f"R-squared (R^2): {r2:.2f}")

# Visualize the mean absolute error
mae = rnn_history.history['mae']
val_mae = rnn_history.history['val_mae']
epochs = range(1,len(mae)+1)

plt.title('Mean Absolute Error')
plt.plot(epochs,mae,label='Train')
plt.plot(epochs,val_mae,color='red',label='Validation')
plt.xlabel('Epochs')
plt.ylabel('MAE')
plt.legend()
plt.show()

"""## Predict"""

# Predict using test sets
y_pred = rnn_model.predict(X_test)
y_pred_inv = min_max_scaler.inverse_transform(y_pred)
y_test_inv = min_max_scaler.inverse_transform(y_test.reshape(-1,1))

print('MAE = ',round(mean_absolute_error(y_true=y_test_inv,y_pred=y_pred_inv),3),' degrees')
print('R2-score = ',round(r2_score(y_test_inv,y_pred_inv),3))

# Visualize prediction
plt.plot(range(1,len(y_test_inv)+1),y_test_inv)
plt.plot(range(1,len(y_pred_inv)+1),y_pred_inv)

"""# Регрессор (LSTM)"""

# Build the LSTM model
lstm_model = tf.keras.Sequential([
    tf.keras.layers.LSTM(10, activation='sigmoid', input_shape=(X_train.shape[1], X_train.shape[2])),
    Dropout(0.2),
    tf.keras.layers.Dense(1, activation='relu')
])

# Compile the LSTM model
lstm_model.compile(loss='mse',
                  optimizer='adam',
                  metrics='mae')

# Train the LSTM model
lstm_history = lstm_model.fit(
    X_train,
    y_train,
    epochs=10,
    batch_size=20,
    validation_data=(X_val, y_val)
)

"""## MSE, MAE, R2"""

# Get R2, MSE, & MAE scores
y_pred = lstm_model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)

mae = mean_absolute_error(y_test, y_pred)

r2 = r2_score(y_test, y_pred)

print(f"MSE: {mse:.2f}")
print(f"MAE: {mae:.2f}")
print(f"R-squared (R^2): {r2:.2f}")

# Visualize the mean absolute error
mae = lstm_history.history['mae']
val_mae = lstm_history.history['val_mae']
epochs = range(1,len(mae)+1)

plt.title('Mean Absolute Error')
plt.plot(epochs,mae,label='Train')
plt.plot(epochs,val_mae,color='red',label='Validation')
plt.xlabel('Epochs')
plt.ylabel('MAE')
plt.legend()
plt.show()

"""## Predict"""

# Predict using test sets
y_pred = lstm_model.predict(X_test)
y_pred_inv = min_max_scaler.inverse_transform(y_pred)
y_test_inv = min_max_scaler.inverse_transform(y_test.reshape(-1,1))

print('MAE = ',round(mean_absolute_error(y_true=y_test_inv,y_pred=y_pred_inv),3),' degrees')
print('R2-score = ',round(r2_score(y_test_inv,y_pred_inv),3))

# Visualize prediction
plt.plot(range(1,len(y_test_inv)+1),y_test_inv)
plt.plot(range(1,len(y_pred_inv)+1),y_pred_inv)

"""# Regressor (LSTM 2 Layers)"""

# Build the LSTM model
lstm_model2 = tf.keras.Sequential([
    tf.keras.layers.LSTM(10, activation='relu', input_shape=(X_train.shape[1], X_train.shape[2]), return_sequences = True),
    Dropout(0.2),
    tf.keras.layers.LSTM(10, activation='sigmoid'),
    Dropout(0.2),
    tf.keras.layers.Dense(1, activation='relu')
])

# Compile the LSTM model
lstm_model2.compile(loss='mse',
                  optimizer='adam',
                  metrics='mae')

# Train the LSTM model
lstm_history2 = lstm_model2.fit(
    X_train,
    y_train,
    epochs=20,
    batch_size=20,
    validation_data=(X_val, y_val)
)

"""## MSE, MAE, R2"""

# Get R2, MSE, & MAE scores
y_pred = lstm_model2.predict(X_test)

mse = mean_squared_error(y_test, y_pred)

mae = mean_absolute_error(y_test, y_pred)

r2 = r2_score(y_test, y_pred)

print(f"MSE: {mse:.2f}")
print(f"MAE: {mae:.2f}")
print(f"R-squared (R^2): {r2:.2f}")

# Visualize the mean absolute error
mae = lstm_history2.history['mae']
val_mae = lstm_history2.history['val_mae']
epochs = range(1,len(mae)+1)

plt.title('Mean Absolute Error')
plt.plot(epochs,mae,label='Train')
plt.plot(epochs,val_mae,color='red',label='Validation')
plt.xlabel('Epochs')
plt.ylabel('MAE')
plt.legend()
plt.show()

"""## Predict"""

# Predict using test sets
y_pred = lstm_model2.predict(X_test)
y_pred_inv = min_max_scaler.inverse_transform(y_pred)
y_test_inv = min_max_scaler.inverse_transform(y_test.reshape(-1,1))

print('MAE = ',round(mean_absolute_error(y_true=y_test_inv,y_pred=y_pred_inv),3),' degrees')
print('R2-score = ',round(r2_score(y_test_inv,y_pred_inv),3))

# Visualize prediction
plt.plot(range(1,len(y_test_inv)+1),y_test_inv)
plt.plot(range(1,len(y_pred_inv)+1),y_pred_inv)