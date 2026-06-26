import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler

from keras.models import Sequential
from keras.layers import LSTM, Dense

class LSTMModel:

    def __init__(self):

        self.scaler = MinMaxScaler()

        self.model = None

    def prepare_data(self, df):

        sales = df["Weekly_Sales"].values.reshape(-1,1)

        scaled = self.scaler.fit_transform(sales)

        X = []
        y = []

        sequence_length = 8

        for i in range(sequence_length, len(scaled)):

            X.append(
                scaled[i-sequence_length:i]
            )

            y.append(
                scaled[i]
            )

        X = np.array(X)
        y = np.array(y)

        return X, y

    def build_model(self):

        model = Sequential()

        model.add(
            LSTM(
                64,
                input_shape=(8,1)
            )
        )

        model.add(
            Dense(1)
        )

        model.compile(

            optimizer="adam",

            loss="mse"

        )

        self.model = model

    def train(self, X, y):

        self.build_model()

        self.model.fit(

            X,

            y,

            epochs=20,

            batch_size=16,

            verbose=1

        )

    def predict(self, X):

        prediction = self.model.predict(X)

        prediction = self.scaler.inverse_transform(
            prediction
        )

        return prediction