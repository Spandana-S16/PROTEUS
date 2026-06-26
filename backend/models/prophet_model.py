import pandas as pd
from prophet import Prophet


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

    def predict_test(self, test_df):

        future = test_df[["Date"]].copy()

        future.rename(
            columns={
                "Date": "ds"
            },
            inplace=True
        )

        forecast = self.model.predict(future)

        return forecast["yhat"].values


if __name__ == "__main__":

    df = pd.read_csv("../data/Walmart_Sales.csv")

    df["Date"] = pd.to_datetime(
        df["Date"],
        dayfirst=True
    )

    store1 = df[df["Store"] == 1]

    model = ProphetModel()

    model.train(store1)

    prediction = model.latest_prediction()

    print("\nLatest Prophet Prediction")
    print(prediction)