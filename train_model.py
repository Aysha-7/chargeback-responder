import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
import joblib

label_col = "CBK"

train_df = pd.read_csv("train.csv")
test_df = pd.read_csv("test.csv")

feature_cols = [c for c in train_df.columns if c != label_col]

X_train = train_df[feature_cols]
y_train = train_df[label_col]
X_test = test_df[feature_cols]
y_test = test_df[label_col]

model = RandomForestClassifier(n_estimators=200, max_depth=8, random_state=42, class_weight="balanced")
model.fit(X_train, y_train)

preds = model.predict(X_test)

precision = precision_score(y_test, preds)
recall = recall_score(y_test, preds)
f1 = f1_score(y_test, preds)
cm = confusion_matrix(y_test, preds)

print("Precision:", round(precision, 3))
print("Recall:", round(recall, 3))
print("F1:", round(f1, 3))
print("Confusion matrix (rows=actual, cols=predicted):")
print(cm)

fp = cm[0][1]
print("False positives:", fp, "out of", cm[0].sum(), "legitimate transactions")

joblib.dump(model, "chargeback_model.pkl")
joblib.dump(feature_cols, "feature_cols.pkl")
print("Model saved.")