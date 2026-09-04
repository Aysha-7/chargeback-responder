import pandas as pd

df = pd.read_csv("archive/df.csv")
print(df.shape)          # rows, columns
print(df.columns.tolist())  # column names
print(df.head())         # first 5 rows
print(df.isnull().sum()) # missing values per column