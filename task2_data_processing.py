import pandas as pd
import os
# ----------------------------------------
# 1 — Load the JSON File
# ----------------------------------------
file_path = "/content/trends_20260413.json"
# ----------------------------------------
# Load JSON into DataFrame
# ----------------------------------------
df = pd.read_json(file_path)
# ----------------------------------------
# Print number of rows loaded
# ----------------------------------------
print(f"Loaded {len(df)} stories from {file_path}")
# ----------------------------------------
# 2 — Clean the Data
# ----------------------------------------
before = len(df)
df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")
# ----------------------------------------
# --- Remove rows with missing critical values ---
# ----------------------------------------
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")
# ----------------------------------------
# Convert score and num_comments to integers
# ----------------------------------------
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)
# ----------------------------------------
# --- Remove low-quality stories ---
# ----------------------------------------
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")
# ----------------------------------------
# Remove leading/trailing spaces
# ----------------------------------------
df["title"] = df["title"].str.strip()
# ----------------------------------------
# 3 — Save as CSV
# ----------------------------------------
os.makedirs("data", exist_ok=True)
output_file = "data/trends_clean.csv"
df.to_csv(output_file, index=False)
print(f"\nSaved {len(df)} rows to {output_file}")
# ----------------------------------------
# Summary: Stories per category
# ----------------------------------------
print("\nStories per category:")
print(df["category"].value_counts())