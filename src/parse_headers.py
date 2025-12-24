import pandas as pd
import re

df = pd.read_csv("data/emails.csv")

def parse_headers(message):
    headers = {}

    def extract(pattern):
        match = re.search(pattern, message, re.IGNORECASE)
        return match.group(1).strip() if match else None

    headers["from"] = extract(r"From:\s*(.*)")
    headers["to"] = extract(r"To:\s*(.*)")
    headers["date"] = extract(r"Date:\s*(.*)")
    headers["subject"] = extract(r"Subject:\s*(.*)")

    return headers

# Test on first 5 emails
for i in range(5):
    parsed = parse_headers(df.loc[i, "message"])
    print(f"\nEmail {i}")
    print(parsed)
