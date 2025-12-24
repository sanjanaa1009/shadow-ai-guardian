import pandas as pd
import re
import networkx as nx
import matplotlib.pyplot as plt
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

G = nx.DiGraph()

for msg in df["message"][:500]:  # limit for visualization
    sender = extract(r"From:\s*(.*)", msg)
    to_field = extract(r"To:\s*(.*)", msg)

    if not sender or not to_field:
        continue

    recipients = [r.strip() for r in to_field.split(",")]
    sens = sensitivity_score(msg)

    for r in recipients:
        if G.has_edge(sender, r):
            G[sender][r]["risk"] += sens
            G[sender][r]["count"] += 1
        else:
            G.add_edge(sender, r, risk=sens, count=1)

# Filter high-risk edges
# ---------------------------------------------------
# CLEAN VISUALIZATION (ONLY TOP HIGH-RISK EDGES)
# ---------------------------------------------------

# Select top risky edges
top_edges = sorted(
    G.edges(data=True),
    key=lambda x: x[2]["risk"],
    reverse=True
)[:15]   # limit to avoid mess

subG = nx.DiGraph()
for u, v, d in top_edges:
    subG.add_edge(u, v, **d)

plt.figure(figsize=(12, 9))

pos = nx.spring_layout(subG, seed=42, k=1.5)

# Draw nodes
nx.draw_networkx_nodes(
    subG,
    pos,
    node_size=1800,
    node_color="lightblue",
    edgecolors="black"
)

# Draw edges
nx.draw_networkx_edges(
    subG,
    pos,
    edge_color="red",
    width=2,
    arrows=True,
    arrowsize=20
)

# Draw labels
nx.draw_networkx_labels(
    subG,
    pos,
    font_size=9,
    font_weight="bold"
)

# Edge labels showing risk score
edge_labels = {
    (u, v): f"risk={d['risk']}"
    for u, v, d in subG.edges(data=True)
}

nx.draw_networkx_edge_labels(
    subG,
    pos,
    edge_labels=edge_labels,
    font_size=8
)

plt.title("High-Risk Email Communication Paths", fontsize=14)
plt.axis("off")
plt.tight_layout()
plt.show()
