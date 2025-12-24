import pandas as pd

SENSITIVE_KEYWORDS = [
    "confidential",
    "salary",
    "account",
    "bank",
    "password",
    "ssn",
    "invoice",
    "contract",
    "legal",
    "deal","sells","purchase"
]

df = pd.read_csv("data/emails.csv")

def is_sensitive(text):
    text = text.lower()
    hits = [kw for kw in SENSITIVE_KEYWORDS if kw in text]
    return len(hits), hits

# Test on few emails
for i in range(5):
    count, words = is_sensitive(df.loc[i, "message"])
    print(f"\nEmail {i}")
    print("Sensitive hits:", count)
    print("Keywords:", words)
