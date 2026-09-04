import json

with open("responses.json") as f:
    results = json.load(f)

tp = sum(1 for r in results if r["action"] == "CONTEST" and r["actual_label_fraud"] == False)
# Here: "CONTEST" = agent thinks merchant should fight it (i.e. predicts NOT fraud/legit dispute)
fp = sum(1 for r in results if r["action"] == "CONTEST" and r["actual_label_fraud"] == True)
fn = sum(1 for r in results if r["action"] == "DO_NOT_CONTEST_REFUND" and r["actual_label_fraud"] == False)
tn = sum(1 for r in results if r["action"] == "DO_NOT_CONTEST_REFUND" and r["actual_label_fraud"] == True)

precision = tp / (tp + fp) if (tp + fp) > 0 else 0
recall = tp / (tp + fn) if (tp + fn) > 0 else 0

print(f"Precision (contest decisions that were correct): {precision:.2f}")
print(f"Recall (correct contests found out of all winnable cases): {recall:.2f}")
print(f"False positives (wrongly told to contest a real fraud case): {fp}")
print(f"Total cases evaluated: {len(results)}")