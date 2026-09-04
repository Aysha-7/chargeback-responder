import pandas as pd
import random
import json

label_col = "CBK"
test_df = pd.read_csv("test.csv")

sample = test_df.sample(n=min(30, len(test_df)), random_state=1).reset_index(drop=True)

cases = []
for i, row in sample.iterrows():
    is_actual_fraud = bool(row[label_col])
    has_delivery_proof = random.random() > (0.8 if is_actual_fraud else 0.2)
    has_matching_chat = random.random() > (0.7 if is_actual_fraud else 0.15)

    case = {
        "case_id": f"CASE-{1000+i}",
        "transaction_amount": float(row["Amount"]),
        "actual_label_fraud": is_actual_fraud,
        "evidence": {
            "delivery_confirmation": "Signed delivery confirmation on file, GPS-tagged, timestamp matches order date." if has_delivery_proof else "No delivery confirmation on file.",
            "customer_chat_log": "Customer messaged support confirming receipt of item on [date]." if has_matching_chat else "No customer communication on file.",
            "refund_policy_shown": "Refund policy was displayed and accepted at checkout." if random.random() > 0.3 else "No record of policy acceptance."
        }
    }
    cases.append(case)

with open("evidence_cases.json", "w") as f:
    json.dump(cases, f, indent=2)

print(f"Generated {len(cases)} synthetic evidence cases -> evidence_cases.json")