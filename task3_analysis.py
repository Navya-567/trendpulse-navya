import pandas as pd
import numpy as np
import os
# ----------------------------------------
# 1 — Load and Explore
# ----------------------------------------
file_path = "data/trends_clean.csv"
df = pd.read_csv(file_path)
print(f"Loaded data: {df.shape}")
print("\nFirst 5 rows:")
print(df.head())
# ----------------------------------------
# Calculate averages
# ----------------------------------------
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()
print(f"\nAverage score : {avg_score:.2f}")
print(f"Average comments: {avg_comments:.2f}")
# ----------------------------------------
# 2 — Basic Analysis with NumPy
# ----------------------------------------
print("\n--- NumPy Stats ---")
scores = df["score"].to_numpy()
comments = df["num_comments"].to_numpy()
# ----------------------------------------
# Mean, Median, Std , Max ,Min
# ----------------------------------------
print(f"Mean score : {np.mean(scores):.2f}")
print(f"Median score : {np.median(scores):.2f}")
print(f"Std deviation: {np.std(scores):.2f}")
print(f"Max score  : {np.max(scores)}")
print(f"Min score  : {np.min(scores)}")
category_counts = df["category"].value_counts()
top_category = category_counts.idxmax()
top_count = category_counts.max()
print(f"\nMost stories in: {top_category} ({top_count} stories)")
max_comments_idx = df["num_comments"].idxmax()
top_story = df.loc[max_comments_idx]
print(f"\nMost commented story: \"{top_story['title']}\" — {top_story['num_comments']} comments")
# ----------------------------------------
# 3 — Add New Columns
# ----------------------------------------
df["engagement"] = df["num_comments"] / (df["score"] + 1)
df["is_popular"] = df["score"] > avg_score
# ----------------------------------------
# 4 — Save the Result
# ----------------------------------------
os.makedirs("data", exist_ok=True)
output_file = "data/trends_analysed.csv"
df.to_csv(output_file, index=False)
print(f"\nSaved to {output_file}")