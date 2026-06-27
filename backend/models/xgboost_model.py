import pandas as pd

from xgboost import XGBRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    mean_absolute_percentage_error
)

from sklearn.model_selection import train_test_split

from backend.utils.feature_engineering import engineer_features


class XGBoostModel:

    def __init__(self):

        self.model = XGBRegressor(

            n_estimators=500,

            learning_rate=0.03,

            max_depth=6,

            subsample=0.8,

            colsample_bytree=0.8,

            random_state=42

        )

        self.is_trained = False

        self.feature_columns = [

            "Store",

            "Holiday_Flag",

            "Fuel_Price",

            "CPI",

            "Unemployment",

            "Year",

            "Month",

            "Week",

            "Quarter",

            "Lag_1",

            "Lag_4",

            "Rolling_Mean_4",

            "Rolling_STD_4",

            "Rolling_CV",

            "Demand_Growth",

            "Demand_Momentum",

            "Fuel_Change",

            "CPI_Change",

            "Unemployment_Change"

        ]


    def prepare_data(self, df):

        df = engineer_features(df.copy())

        df.dropna(inplace=True)

        X = df[self.feature_columns]

        y = df["Weekly_Sales"]

        return X, y


    def train(self, df):

        X, y = self.prepare_data(df)

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(

            X,

            y,

            test_size=0.2,

            random_state=42,

            shuffle=False

        )

        self.model.fit(

            self.X_train,

            self.y_train

        )

        self.is_trained = True


    def predict(self, X=None):

        if not self.is_trained:

            raise Exception("Model has not been trained.")

        if X is None:

            X = self.X_test

        return self.model.predict(X)


    def latest_prediction(self):

        latest_features = self.X_test.tail(1)

        prediction = self.model.predict(

            latest_features

        )

        return float(prediction[0])


    def evaluate(self):

        predictions = self.predict()

        mae = mean_absolute_error(

            self.y_test,

            predictions

        )

        rmse = mean_squared_error(

            self.y_test,

            predictions

        ) ** 0.5

        mape = mean_absolute_percentage_error(

            self.y_test,

            predictions

        ) * 100

        return {

            "MAE": round(float(mae), 2),

            "RMSE": round(float(rmse), 2),

            "MAPE": round(float(mape), 2)

        }


if __name__ == "__main__":

    df = pd.read_csv(

        "data/DataCo_Weekly.csv"

    )

    df["Date"] = pd.to_datetime(

        df["Date"]
    )

    model = XGBoostModel()

    model.train(df)

    metrics = model.evaluate()

    prediction = model.latest_prediction()

    print("\n========== XGBOOST ==========")

    print("\nMetrics")

    print(metrics)

    print("\nLatest Prediction")

    print(round(float(prediction), 2))