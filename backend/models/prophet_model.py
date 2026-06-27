import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
from sklearn.metrics import mean_absolute_percentage_error

class ProphetModel:

    def __init__(self):
        self.model = Prophet()
        self.is_trained = False

    def prepare_data(self, df):
        """
        Converts dataframe into Prophet format.
        """

        prophet_df = df[["Date", "Weekly_Sales"]].copy()

        prophet_df.rename(
            columns={
                "Date": "ds",
                "Weekly_Sales": "y"
            },
            inplace=True
        )

        return prophet_df

    def train(self, df):
        """
        Train Prophet on the supplied dataframe.
        """

        prophet_df = self.prepare_data(df)

        self.model.fit(prophet_df)

        self.is_trained = True

    def forecast(self, periods=12):
        """
        Forecast future demand.
        """

        if not self.is_trained:
            raise Exception("Prophet model has not been trained.")

        future = self.model.make_future_dataframe(
            periods=periods,
            freq="W"
        )

        forecast = self.model.predict(future)

        return forecast

    def predict(self, periods=1):
        """
        Return only the predicted demand values.
        """

        forecast = self.forecast(periods)

        return forecast[["ds", "yhat"]]

    def latest_prediction(self):
        """
        Returns the latest predicted demand.
        """

        forecast = self.forecast(periods=1)

        return forecast.iloc[-1]["yhat"]

    def predict_test(self, train_df, test_df):

        predictions = []

        stores = sorted(test_df["Store"].unique())

        for store in stores:

            print(f"Prophet -> Store {store}")

            train_store = train_df[
                train_df["Store"] == store
            ].copy()

            test_store = test_df[
                test_df["Store"] == store
            ].copy()

            if len(train_store) == 0 or len(test_store) == 0:
                continue

            prophet_df = self.prepare_data(train_store)

            model = Prophet()

            model.fit(prophet_df)

            future = pd.DataFrame({
                "ds": test_store["Date"]
            })

            forecast = model.predict(future)

            predictions.extend(
                forecast["yhat"].values
            )

        return predictions
    
    def evaluate(self, df):

        if not self.is_trained:
            raise Exception("Model has not been trained.")

        prophet_df = self.prepare_data(df)

        predictions = self.model.predict(
            prophet_df[["ds"]]
        )

        actual = prophet_df["y"].values

        predicted = predictions["yhat"].values

        mae = mean_absolute_error(
            actual,
            predicted
        )

        rmse = np.sqrt(
            mean_squared_error(
                actual,
                predicted
            )
        )

        mape = mean_absolute_percentage_error(
            actual,
            predicted
        ) * 100

        return {

            "MAE": round(float(mae),2),

            "RMSE": round(float(rmse),2),

            "MAPE": round(float(mape),2)

        }


if __name__ == "__main__":

    df = pd.read_csv("data/DataCo_Weekly.csv")

    df["Date"] = pd.to_datetime(
        df["Date"]
    )

    model = ProphetModel()

    model.train(df)

    print("\n========== PROPHET ==========")

    print("\nMetrics")

    print(model.evaluate(df))

    print("\nLatest Prediction")

    print(round(model.latest_prediction(),2))