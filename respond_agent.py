import json
import random

with open("evidence_cases.json") as f:
    cases = json.load(f)

def build_response_letter(case_id, evidence, strong_points):
    """
    Builds a dispute evidence response letter from templated clauses.
    Only includes clauses backed by evidence actually present in the case —
    never invents evidence, which avoids the hallucination risk of a free-text LLM.
    """
    opening = f"Re: Dispute Case {case_id}\n\nWe are submitting evidence in response to the above chargeback claim.\n"

    clauses = []
    if "No " not in evidence["delivery_confirmation"]:
        clauses.append(f"- Delivery evidence: {evidence['delivery_confirmation']}")
    if "No " not in evidence["customer_chat_log"]:
        clauses.append(f"- Customer communication: {evidence['customer_chat_log']}")
    if "No record" not in evidence["refund_policy_shown"]:
        clauses.append(f"- Policy acknowledgement: {evidence['refund_policy_shown']}")

    body = "\n".join(clauses)

    closing = (
        f"\n\nBased on the {strong_points} piece(s) of evidence above, we respectfully "
        f"request that this chargeback be reversed in favor of the merchant.\n\nSincerely,\nMerchant Risk Team"
    )

    return opening + body + closing


results = []

for case in cases:
    try:
        evidence = case["evidence"]

        strong_points = sum([
            "No " not in evidence["delivery_confirmation"],
            "No " not in evidence["customer_chat_log"],
            "No record" not in evidence["refund_policy_shown"]
        ])

        winnable = strong_points >= 2
        confidence = round(strong_points / 3, 2)
        action = "CONTEST" if winnable else "DO_NOT_CONTEST_REFUND"

        response_letter = None
        if winnable:
            response_letter = build_response_letter(case["case_id"], evidence, strong_points)

        results.append({
            "case_id": case["case_id"],
            "action": action,
            "confidence": confidence,
            "actual_label_fraud": case["actual_label_fraud"],
            "response_letter": response_letter
        })

    except Exception as e:
        # Graceful failure: incomplete case data shouldn't crash the whole batch —
        # flag it for manual review instead
        print(f"[HANDLED FAILURE] Could not process {case.get('case_id', 'UNKNOWN')}: {e}. Flagging for manual review.")
        results.append({
            "case_id": case.get("case_id", "UNKNOWN"),
            "action": "MANUAL_REVIEW_REQUIRED",
            "confidence": 0.0,
            "actual_label_fraud": case.get("actual_label_fraud"),
            "response_letter": None
        })

with open("responses.json", "w") as f:
    json.dump(results, f, indent=2)

audit_log = []
for r in results:
    audit_log.append({
        "case_id": r["case_id"],
        "decision": r["action"],
        "confidence": r["confidence"],
        "reasoning": f"Decision based on {sum([1 for k in ['delivery_confirmation','customer_chat_log','refund_policy_shown']])} evidence signals evaluated.",
        "human_review_required": r["confidence"] < 0.5  # low-confidence cases get flagged for a human, not auto-actioned
    })

with open("audit_log.json", "w") as f:
    json.dump(audit_log, f, indent=2)

print("Audit log written -> audit_log.json")
print(f"Processed {len(results)} cases -> responses.json")
for r in results[:3]:
    print(json.dumps(r, indent=2))