import pandas as pd

from models.lstm_model import LSTMModel

df = pd.read_csv("../data/Walmart_Sales.csv")

df["Date"] = pd.to_datetime(
    df["Date"],
    dayfirst=True
)

df = df[df["Store"] == 1]

model = LSTMModel()

X, y = model.prepare_data(df)

print("Training samples:", X.shape)

model.train(X,y)

prediction = model.predict(X[-1:])

print("\nLatest Prediction")

print(prediction)