import pandas as pd

from backend.utils.feature_engineering import engineer_features


class GatingDatasetBuilder:

    def __init__(self):
        pass

    def load_data(self):

        df = pd.read_csv("data/Walmart_Sales.csv")

        df["Date"] = pd.to_datetime(
            df["Date"],
            dayfirst=True
        )

        return df

    def prepare_dataset(self):

        df = self.load_data()

        # Feature Engineering
        df = engineer_features(df)

        # Context features for gating network
        context = df[
            [
                "Date",
                "Store",
                "Holiday_Flag",
                "Month",
                "Quarter",
                "Rolling_CV",
                "Demand_Growth",
                "Demand_Momentum",
                "Fuel_Change",
                "CPI_Change",
                "Unemployment_Change",
                "Weekly_Sales"
            ]
        ].copy()

        # Remove rows where rolling features are NaN
        context.dropna(inplace=True)

        return context

    def save_dataset(self):

        dataset = self.prepare_dataset()

        dataset.to_csv(
            "gating_dataset.csv",
            index=False
        )

        print("\nDataset Created Successfully!")

        print(f"\nSamples : {len(dataset)}")

        print("\nColumns")

        print(dataset.columns)

        print("\nPreview")

        print(dataset.head())


if __name__ == "__main__":

    builder = GatingDatasetBuilder()

    builder.save_dataset()