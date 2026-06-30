import pandas as pd
import numpy as np
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error


class ProphetModel:

    def __init__(self):
        self.model = Prophet()
        self.is_trained = False

    def prepare_data(self, df):

        prophet_df = df[["Date", "Weekly_Sales"]].copy()

        prophet_df.rename(
            columns={"Date": "ds", "Weekly_Sales": "y"},
            inplace=True
        )

        prophet_df = prophet_df.sort_values("ds").reset_index(drop=True)

        prophet_df["y"] = prophet_df["y"].clip(lower=0)

        return prophet_df

    def _fill_gaps(self, store_df):
        """
        ROOT CAUSE FIX: DataCo has massive internal date gaps per store
        (up to 602 days for Caribbean, South America, Central America).

        When Prophet trains on a series with a 602-day hole in the middle,
        it fits a linear trend ACROSS the gap. If demand rises before the
        gap and falls after, Prophet extrapolates a sharply declining trend
        into the test period — producing negative or wildly wrong predictions.

        Fix: resample to a complete weekly grid and interpolate missing values
        linearly. Prophet now sees a continuous series and fits a stable trend.
        """

        store_df = store_df.sort_values("Date").reset_index(drop=True)

        full_range = pd.date_range(
            start=store_df["Date"].min(),
            end=store_df["Date"].max(),
            freq="W"
        )

        full_df = pd.DataFrame({"Date": full_range})

        full_df = full_df.merge(
            store_df[["Date", "Weekly_Sales"]],
            on="Date",
            how="left"
        )

        full_df["Weekly_Sales"] = full_df["Weekly_Sales"].interpolate(
            method="linear"
        )

        # Copy store identifier back
        full_df["Store"] = store_df["Store"].iloc[0]

        return full_df

    def train(self, df):

        prophet_df = self.prepare_data(df)

        self.model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=False,
            daily_seasonality=False,
            changepoint_prior_scale=0.05,
            seasonality_prior_scale=10,
        )

        self.model.fit(prophet_df)

        self.is_trained = True

    def forecast(self, periods=12):

        if not self.is_trained:
            raise Exception("Prophet model has not been trained.")

        future = self.model.make_future_dataframe(periods=periods, freq="W")

        forecast = self.model.predict(future)

        return forecast

    def predict(self, periods=1):

        forecast = self.forecast(periods)

        return forecast[["ds", "yhat"]]

    def latest_prediction(self):

        forecast = self.forecast(periods=1)

        return forecast.iloc[-1]["yhat"]

    def predict_test(self, train_df, test_df):
        """
        Predict on held-out test rows for each store independently.

        Two fixes applied here:
        1. Gap filling (_fill_gaps) — prevents negative extrapolation from
           stores with massive internal date voids (up to 602 days).
        2. Merge-based alignment — predictions are matched back to test_df
           by (Store, Date) key, not by positional index. This guarantees
           correct alignment even if a store is skipped, so no store's
           predictions land on a different store's rows.
        """

        all_preds = []

        stores = sorted(test_df["Store"].unique())

        for store in stores:

            print(f"Prophet -> {store}")

            train_store = train_df[
                train_df["Store"] == store
            ].copy().sort_values("Date").reset_index(drop=True)

            test_store = test_df[
                test_df["Store"] == store
            ].copy().sort_values("Date").reset_index(drop=True)

            if len(train_store) < 4 or len(test_store) == 0:
                print(f"  Skipping {store} — insufficient data, filling with median")
                fallback = float(train_df["Weekly_Sales"].median())
                test_store = test_store.copy()
                test_store["Prophet_Prediction"] = fallback
                all_preds.append(test_store[["Store", "Date", "Prophet_Prediction"]])
                continue

            # FIX 1: fill internal date gaps before fitting Prophet
            filled_train = self._fill_gaps(train_store)

            prophet_df = self.prepare_data(filled_train)

            model = Prophet(
                yearly_seasonality=True,
                weekly_seasonality=False,
                daily_seasonality=False,
                changepoint_prior_scale=0.05,
                seasonality_prior_scale=10,
            )

            model.fit(prophet_df)

            future = pd.DataFrame({"ds": pd.to_datetime(test_store["Date"].values)})

            forecast = model.predict(future)

            # Clip negatives — demand cannot be negative
            forecast["yhat"] = forecast["yhat"].clip(lower=0)

            # Cap at 1.5x max training sales to prevent wild extrapolation
            cap = float(train_store["Weekly_Sales"].max()) * 1.5
            forecast["yhat"] = forecast["yhat"].clip(upper=cap)

            test_store = test_store.copy()
            test_store["Prophet_Prediction"] = forecast["yhat"].values

            all_preds.append(test_store[["Store", "Date", "Prophet_Prediction"]])

        # FIX 2: merge back by Store + Date, not by positional index
        # This makes alignment structurally impossible to get wrong
        preds_df = pd.concat(all_preds, ignore_index=True)

        test_df = test_df.copy()

        test_df = test_df.merge(
            preds_df,
            on=["Store", "Date"],
            how="left"
        )

        # Any remaining NaN -> global median fallback
        fallback = float(train_df["Weekly_Sales"].median())
        test_df["Prophet_Prediction"] = test_df["Prophet_Prediction"].fillna(fallback)

        return test_df["Prophet_Prediction"].tolist()

    def evaluate(self, df):

        if not self.is_trained:
            raise Exception("Model has not been trained.")

        prophet_df = self.prepare_data(df)

        predictions = self.model.predict(prophet_df[["ds"]])

        actual = prophet_df["y"].values
        predicted = predictions["yhat"].values

        mae = mean_absolute_error(actual, predicted)
        rmse = np.sqrt(mean_squared_error(actual, predicted))
        mape = mean_absolute_percentage_error(actual, predicted) * 100

        return {
            "MAE": round(float(mae), 2),
            "RMSE": round(float(rmse), 2),
            "MAPE": round(float(mape), 2)
        }


if __name__ == "__main__":

    df = pd.read_csv("data/DataCo_Weekly.csv")

    df["Date"] = pd.to_datetime(df["Date"])

    model = ProphetModel()

    model.train(df)

    print("\n========== PROPHET ==========")
    print("\nMetrics")
    print(model.evaluate(df))
    print("\nLatest Prediction")
    print(round(model.latest_prediction(), 2))