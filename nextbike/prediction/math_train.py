from .. import io
import numpy as np
import warnings

from sklearn.linear_model import LinearRegression
from sklearn import svm
from tensorflow import keras
from tensorflow.keras import layers
from sklearn import metrics


# TODO: Add docstring
def train_linear_regression(p_X_train_scaled, p_y_train):
    lin = LinearRegression()
    lin.fit(p_X_train_scaled, p_y_train)
    io.save_object(lin, "Linear_Regression_Model.pkl")
    y_prediction = lin.predict(p_X_train_scaled)
    show_error_metrics(p_y_train, y_prediction, "Linear_Regression_Model", lin.score(p_X_train_scaled, p_y_train))


def train_neural_network(p_X_train_scaled, p_y_train):
    """train neural network

    Args:
        p_X_train_scaled (DataFrame): Scaled x input of train set
        p_y_train (Series): y output to train on
    Returns:
        no return
    """
    neural_network = keras.Sequential(
        [layers.Dense(36, activation="relu", input_shape=[p_X_train_scaled.shape[1]]),
         # layers.Dropout(0.2),
         layers.Dense(36, activation="relu"),
         # layers.Dropout(0.2),
         layers.Dense(1)])
    optimizer = keras.optimizers.RMSprop(0.001)
    neural_network.compile(loss="mse",
                           optimizer=optimizer,
                           metrics=["mae", "mse"])
    epochs = 10
    # batch_size = 200  # right now not used but should be tried
    neural_network.fit(p_X_train_scaled, p_y_train.values, epochs=epochs, validation_split=0.2)
    neural_network.save(io.get_path("Neural_Network_Model", "output", "models"))
    y_prediction = neural_network.predict(p_X_train_scaled)
    show_error_metrics(p_y_train, y_prediction, "Neural_Network_Model")


def train_svm(p_X_train_scaled, p_y_train):
    """Trains a svm

    Args:
        p_X_train_scaled (DataFrame): Scaled x input of train set
        p_y_train (Series): y output to train on
    Returns:
        no return
    """
    warnings.filterwarnings('ignore', 'Solver terminated early.*')
    # specify kernel{‘linear’, ‘poly’, ‘rbf’, ‘sigmoid’, ‘precomputed’}, default=’rbf’
    # degreeint, default=3
    # max_iterint, default=-1 => no limit
    # verbose=1
    regr = svm.SVR(kernel="linear", max_iter=1000, cache_size=2000, degree=1, gamma="auto")  # max_iter=5000 lot better
    regr.fit(p_X_train_scaled, p_y_train)
    io.save_object(regr, "SVM_Regression_Model_" + str(3) + ".pkl")
    y_prediction = regr.predict(p_X_train_scaled)
    show_error_metrics(p_y_train, y_prediction, "SVM_Regression_Model_3", regr.score(p_X_train_scaled, p_y_train))


def show_error_metrics(p_y_true, p_y_predictions, p_filename, p_score=None):
    print(p_filename, "Training loss - Error Metrics:")
    print("RMSE:", np.sqrt(metrics.mean_squared_error(p_y_true, p_y_predictions)), end=" ")
    print("MAE", metrics.mean_absolute_error(p_y_true, p_y_predictions), end=" ")
    print("R^2:", p_score)
