import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error

from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Input
from keras.callbacks import EarlyStopping

from backend.utils.feature_engineering import engineer_features


class LSTMModel:

    def __init__(self):

        self.sequence_length = 8

        self.scaler = MinMaxScaler()

        self.model = None

        self.is_trained = False

    def prepare_data(self, df):

        df = engineer_features(df.copy())

        df.dropna(inplace=True)

        sales = df["Weekly_Sales"].values.reshape(-1, 1)

        scaled = self.scaler.fit_transform(sales)

        X = []
        y = []

        for i in range(self.sequence_length, len(scaled)):

            X.append(
                scaled[i-self.sequence_length:i]
            )

            y.append(
                scaled[i]
            )

        X = np.array(X)
        y = np.array(y)

        split = int(len(X) * 0.8)

        self.X_train = X[:split]
        self.X_test = X[split:]

        self.y_train = y[:split]
        self.y_test = y[split:]

    def build_model(self):

        model = Sequential()

        model.add(
            Input(shape=(self.sequence_length,1))
        )

        model.add(
            LSTM(
                64,
                return_sequences=True
            )
        )

        model.add(
            Dropout(0.2)
        )

        model.add(
            LSTM(32)
        )

        model.add(
            Dense(16, activation="relu")
        )

        model.add(
            Dense(1)
        )

        model.compile(

            optimizer="adam",

            loss="mse"

        )

        self.model = model

    def train(self, df):

        self.prepare_data(df)

        self.build_model()

        callback = EarlyStopping(

            monitor="loss",

            patience=5,

            restore_best_weights=True

        )

        self.model.fit(

            self.X_train,

            self.y_train,

            epochs=50,

            batch_size=16,

            verbose=1,

            callbacks=[callback]

        )

        self.is_trained = True

    def predict(self):

        if not self.is_trained:

            raise Exception("Model not trained.")

        prediction = self.model.predict(

            self.X_test,

            verbose=0

        )

        prediction = self.scaler.inverse_transform(

            prediction

        )

        return prediction

    def latest_prediction(self):

        prediction = self.model.predict(

            self.X_test[-1].reshape(1,self.sequence_length,1),

            verbose=0

        )

        prediction = self.scaler.inverse_transform(

            prediction

        )

        return float(prediction[0][0])

    def evaluate(self):

        predictions = self.predict()

        actual = self.scaler.inverse_transform(

            self.y_test.reshape(-1,1)

        )

        mae = mean_absolute_error(

            actual,

            predictions

        )

        rmse = np.sqrt(

            mean_squared_error(

                actual,

                predictions

            )

        )

        return {

            "MAE": round(mae,2),

            "RMSE": round(rmse,2)

        }


if __name__ == "__main__":

    df = pd.read_csv(

        "data/Walmart_Sales.csv"

    )

    df["Date"] = pd.to_datetime(

        df["Date"],

        dayfirst=True

    )

    model = LSTMModel()

    model.train(df)

    print("\n========== LSTM ==========")

    print("\nMetrics")

    print(model.evaluate())

    print("\nLatest Prediction")

    print(round(model.latest_prediction(),2))