import pandas as pd
import re
from collections import defaultdict
from datetime import datetime

# -----------------------------
# CONFIG
# -----------------------------
CSV_PATH = "data/emails.csv"

SENSITIVE_KEYWORDS = [
    "confidential", "salary", "account",
    "bank", "password", "ssn",
    "invoice", "contract", "legal"
]

# -----------------------------
# HELPERS
# -----------------------------
def extract_field(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else None

def sensitivity_score(text):
    text = text.lower()
    return sum(1 for k in SENSITIVE_KEYWORDS if k in text)

def parse_date(date_str):
    try:
        return datetime.strptime(
            date_str.split("(")[0].strip(),
            "%a, %d %b %Y %H:%M:%S %z"
        ).isoformat()
    except:
        return None

def get_domain(email):
    return email.split("@")[-1].lower() if "@" in email else None

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv(CSV_PATH)

nodes = {}
edges = {}

# -----------------------------
# BUILD GRAPH
# -----------------------------
for msg in df["message"]:
    sender = extract_field(r"From:\s*(.*)", msg)
    to_field = extract_field(r"To:\s*(.*)", msg)
    date_field = extract_field(r"Date:\s*(.*)", msg)

    if not sender or not to_field:
        continue

    recipients = [r.strip() for r in to_field.split(",")]
    risk = sensitivity_score(msg)
    timestamp = parse_date(date_field)

    # Register sender node
    if sender not in nodes:
        nodes[sender] = {
            "email": sender,
            "domain": get_domain(sender),
            "is_external": not sender.lower().endswith("@enron.com")
        }

    for r in recipients:
        # Register recipient node
        if r not in nodes:
            nodes[r] = {
                "email": r,
                "domain": get_domain(r),
                "is_external": not r.lower().endswith("@enron.com")
            }

        edge_key = (sender, r)

        if edge_key not in edges:
            edges[edge_key] = {
                "from": sender,
                "to": r,
                "count": 0,
                "risk": 0,
                "last_timestamp": timestamp
            }

        edges[edge_key]["count"] += 1
        edges[edge_key]["risk"] += risk

        if timestamp:
            edges[edge_key]["last_timestamp"] = timestamp

# -----------------------------
# OUTPUT
# -----------------------------
graph_data = {
    "nodes": list(nodes.values()),
    "edges": list(edges.values())
}

print("Graph build complete")
print(f"Total nodes: {len(graph_data['nodes'])}")
print(f"Total edges: {len(graph_data['edges'])}")

# Optional: return graph_data if imported
if __name__ == "__main__":
    pass
