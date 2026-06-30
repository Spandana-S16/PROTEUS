import pandas as pd

df = pd.read_csv("data/DataCo_Weekly.csv")

print(df.groupby("Store").size())
print("\nTotal Stores:", df["Store"].nunique())