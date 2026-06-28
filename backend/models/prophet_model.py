import pandas as pd
import numpy as np

from prophet import Prophet

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    mean_absolute_percentage_error
)


class ProphetModel:

    def __init__(self):

        self.models = {}

        self.is_trained = False

    def prepare_data(self, df):

        prophet_df = df[
            ["Date", "Weekly_Sales"]
        ].copy()

        prophet_df.rename(
            columns={
                "Date": "ds",
                "Weekly_Sales": "y"
            },
            inplace=True
        )

        prophet_df = prophet_df.sort_values("ds").reset_index(drop=True)

        prophet_df["y"] = prophet_df["y"].clip(lower=0)

        return prophet_df

    def train(self, df):

        self.models = {}

        self.training_data = {}

        stores = sorted(df["Store"].unique())

        print("\nTraining Prophet Models")

        for store in stores:

            print(f"Training -> {store}")

            store_df = df[
                df["Store"] == store
            ].copy()

            store_df = store_df.sort_values("Date").reset_index(drop=True)

            self.training_data[store] = store_df

            if len(store_df) < 8:
                print(f"  Skipping {store} — only {len(store_df)} rows")
                continue

            prophet_df = self.prepare_data(store_df)

            model = Prophet(

                yearly_seasonality=True,

                weekly_seasonality=False,

                daily_seasonality=False,

                changepoint_prior_scale=0.05,

                seasonality_prior_scale=10,

                interval_width=0.95

            )

            model.fit(prophet_df)

            self.models[store] = model

        self.is_trained = True

    def forecast(self, periods=1):

        if not self.is_trained:
            raise Exception("Prophet model has not been trained.")

        forecasts = {}

        for store, model in self.models.items():

            future = model.make_future_dataframe(
                periods=periods,
                freq="W"
            )

            forecast = model.predict(future)

            forecast["yhat"] = forecast["yhat"].clip(lower=0)

            forecasts[store] = forecast

        return forecasts

    def predict(self, periods=1):

        return self.forecast(periods)

    def latest_prediction(self):

        forecasts = self.forecast(periods=1)

        total_prediction = 0

        for store, forecast in forecasts.items():

            history = self.training_data[store]["Weekly_Sales"]

            max_sales = history.max()

            median_sales = history.median()

            cap = max(
                max_sales * 1.10,
                median_sales * 2
            )

            prediction = float(forecast.iloc[-1]["yhat"])

            prediction = max(0.0, prediction)

            prediction = min(prediction, cap)

            print(store, prediction)

            total_prediction += prediction

        return round(total_prediction, 2)

    def predict_test(self, train_df, test_df):
        """
        Predict on test set for each store independently.

        FIX: predictions are collected into a DataFrame keyed by
        (Store, Date) and merged back to test_df. This guarantees
        correct alignment even when some stores are skipped due to
        insufficient training data (the original bug caused 26/89
        zero predictions from index misalignment after skipped stores).
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

            if len(train_store) < 8:
                print(f"  Skipping {store} — only {len(train_store)} train rows, filling with median")
                # Fill with training median of all stores as fallback
                fallback = train_df["Weekly_Sales"].median()
                test_store["Prophet_Prediction"] = fallback
                all_preds.append(
                    test_store[["Store", "Date", "Prophet_Prediction"]]
                )
                continue

            prophet_df = self.prepare_data(train_store)

            model = Prophet(

                yearly_seasonality=True,

                weekly_seasonality=False,

                daily_seasonality=False,

                changepoint_prior_scale=0.05,

                seasonality_prior_scale=10

            )

            model.fit(prophet_df)

            future = pd.DataFrame({"ds": test_store["Date"].values})

            print(f"  Train end : {prophet_df['ds'].max()}")
            print(f"  Test start: {future['ds'].min()}")

            forecast = model.predict(future)

            forecast["yhat"] = forecast["yhat"].clip(lower=0)

            # Cap predictions to prevent extreme extrapolation
            max_train_sales = train_store["Weekly_Sales"].max()
            forecast["yhat"] = forecast["yhat"].clip(
                upper=max_train_sales * 1.5
            )

            test_store = test_store.copy()
            test_store["Prophet_Prediction"] = forecast["yhat"].values

            all_preds.append(
                test_store[["Store", "Date", "Prophet_Prediction"]]
            )

        # Merge predictions back to test_df by Store + Date
        # This is the critical fix: no index misalignment possible
        preds_df = pd.concat(all_preds, ignore_index=True)

        test_df = test_df.copy()

        test_df = test_df.merge(
            preds_df,
            on=["Store", "Date"],
            how="left"
        )

        # Any remaining NaN (edge cases) → global median
        median_fallback = train_df["Weekly_Sales"].median()
        test_df["Prophet_Prediction"] = test_df["Prophet_Prediction"].fillna(
            median_fallback
        )

        return test_df["Prophet_Prediction"].tolist()

    def evaluate(self, df):

        if not self.is_trained:
            raise Exception("Model has not been trained.")

        actual = []

        predicted = []

        stores = sorted(df["Store"].unique())

        for store in stores:

            if store not in self.models:
                continue

            store_df = df[
                df["Store"] == store
            ].copy()

            prophet_df = self.prepare_data(store_df)

            model = self.models[store]

            forecast = model.predict(
                prophet_df[["ds"]]
            )

            forecast["yhat"] = forecast[
                "yhat"
            ].clip(lower=0)

            actual.extend(
                prophet_df["y"].tolist()
            )

            predicted.extend(
                forecast["yhat"].tolist()
            )

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

    print(model.latest_prediction())