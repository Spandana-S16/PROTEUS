import pandas as pd
from prophet import Prophet

# Load dataset
df = pd.read_csv("../data/Walmart_Sales.csv")

print("Dataset Shape:", df.shape)
print("Dataset Columns:", df.columns)

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)

print("\nData Types:")
print(df.dtypes)

# Filter data for Store 1
store1 = df[df["Store"] == 1]

# Prophet requires columns named 'ds' and 'y'
prophet_df = store1[["Date", "Weekly_Sales"]].rename(
    columns={
        "Date": "ds",
        "Weekly_Sales": "y"
    }
)

print("\nTraining Data:")
print(prophet_df.head())

# Train Prophet model
model = Prophet()
model.fit(prophet_df)

# Forecast next 12 weeks
future = model.make_future_dataframe(
    periods=12,
    freq="W"
)

forecast = model.predict(future)

print("\nNext 12 Week Forecast:")
print(forecast[["ds", "yhat"]].tail(12))