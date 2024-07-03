import pandas as pd
import matplotlib
import numpy as np

df = pd.read_csv("dataset/", skiprows=20, parse_dates=["    DATE"])

query = df["TG0"] = df["   TG"].mask(df["   TG"] == -9999, np.nan)
query = df["TG"] = df["TG0"] / 10
query = df["Farenheit"] = df["TG"] * (9/5) + 32

df
print(df)
