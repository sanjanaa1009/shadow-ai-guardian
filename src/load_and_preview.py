import pandas as pd

# Load CSV
df = pd.read_csv("data/emails.csv")

# Show basic info
print("Shape:", df.shape)
print("\nColumns:")
print(df.columns)

print("\nSample rows:")
print(df.head(3))
