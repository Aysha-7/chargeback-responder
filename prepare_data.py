import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("archive/df.csv")

# Convert the label from Yes/No text to 1/0 numbers
df["CBK"] = df["CBK"].map({"Yes": 1, "No": 0})

# Turn the Date column into useful numeric features
df["Date"] = pd.to_datetime(df["Date"])
df["hour"] = df["Date"].dt.hour
df["day_of_week"] = df["Date"].dt.dayofweek

# Count how many times each card appears (cards used many times in short span can be a fraud signal)
df["card_txn_count"] = df.groupby("Card Number")["Card Number"].transform("count")

# Drop columns we can't use directly as numeric features
df = df.drop(columns=["Unnamed: 0", "Card Number", "Date"])

# Split into train (80%) and held-out test (20%)
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df["CBK"])

train_df.to_csv("train.csv", index=False)
test_df.to_csv("test.csv", index=False)

print("Train size:", len(train_df))
print("Test size:", len(test_df))
print("Fraud rate in train:", train_df["CBK"].mean())
print("Fraud rate in test:", test_df["CBK"].mean())