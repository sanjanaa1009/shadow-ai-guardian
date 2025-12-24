import pandas as pd
import re
from collections import defaultdict

SENSITIVE_KEYWORDS = [
    "confidential", "salary", "account",
    "bank", "password", "ssn",
    "invoice", "contract", "legal"
]

df = pd.read_csv("data/emails.csv")

def extract(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else None

def sensitivity_score(text):
    text = text.lower()
    return sum(1 for k in SENSITIVE_KEYWORDS if k in text)

edge_risk = defaultdict(int)

for msg in df["message"]:
    sender = extract(r"From:\s*(.*)", msg)
    to_field = extract(r"To:\s*(.*)", msg)

    if not sender or not to_field:
        continue

    recipients = [r.strip() for r in to_field.split(",")]
    sens_score = sensitivity_score(msg)

    for r in recipients:
        edge_risk[(sender, r)] += sens_score

# Show top risky edges
sorted_risks = sorted(edge_risk.items(), key=lambda x: x[1], reverse=True)

print(" Top risky communication paths:")
for edge, score in sorted_risks[:5]:
    print(edge, "Risk Score:", score)

