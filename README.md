
# Chargeback Evidence Responder

An agent that classifies disputed transactions as winnable/not winnable, drafts evidence-based
dispute responses for winnable cases, and logs every decision for audit — built for the
Razorpay AI Buildathon, AI Risk Manager track.

## Problem
Merchants lose revenue to chargebacks even when they have evidence to win the dispute, because
compiling and drafting a response is manual and slow.

## Approach
1. A Random Forest classifier trained on [dataset name + link], a real chargeback-labeled
   transaction dataset, flags fraud risk. Held-out test set metrics: Precision X, Recall X, F1 X.
2. A separate evidence-scoring step evaluates dispute-specific evidence (delivery confirmation,
   customer communication, policy acceptance) to decide CONTEST vs REFUND.
3. For winnable cases, a rule-based template engine drafts a short evidence response citing only
   the evidence on file. This is deterministic by design: it cannot hallucinate evidence that
   doesn't exist in the case record, which matters for a compliance-sensitive workflow like this.
4. Every decision is logged to `audit_log.json` with reasoning and a confidence score; low-confidence
   cases are flagged for human review rather than auto-actioned.

## Data note
Real transaction/fraud labels come from [dataset link]. Chargeback-specific evidence documents
(delivery logs, chat transcripts) are not publicly available for privacy/proprietary reasons, so
these are synthetically generated on top of the real transaction records — see `generate_evidence.py`
for the exact generation logic.

## Results
- Classifier: Precision X, Recall X, F1 X on held-out test set (N=X transactions)
- Evidence responder: Precision X, Recall X on N=30 synthetic dispute cases
- False positive cost: [your honest note on what a wrong CONTEST costs the merchant]

## Limitations
- Evidence data is synthetic, not real dispute records
- Bounded to defense-only actions, no offensive/automated retaliation capability
- Low-confidence cases require human review, not fully autonomous

## How to run
[list the exact commands: pip install -r requirements.txt, python prepare_data.py, python train_model.py, python generate_evidence.py, python respond_agent.py, python evaluate.py]
```

Save this file, then push it too:
```
git add README.md
git commit -m "Add README"
git push
```
