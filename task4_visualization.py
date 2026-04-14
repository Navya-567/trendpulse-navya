import pandas as pd
import matplotlib.pyplot as plt
import os
# ----------------------------------------
# 1 — Setup
# ----------------------------------------
file_path = "data/trends_analysed.csv"
df = pd.read_csv(file_path)
os.makedirs("outputs", exist_ok=True)
def shorten_title(title, max_len=50):
  return title if len(title) <= max_len else title[:47] + "..."
# ----------------------------------------
# 2 — Chart 1: Top 10 Stories by Score
# ----------------------------------------
top10 = df.sort_values(by="score", ascending=False).head(10)
top10["short_title"] = top10["title"].apply(shorten_title)
# ----------------------------------------
# Plot horizontal bar chart
# ----------------------------------------
plt.figure()
plt.barh(top10["short_title"], top10["score"])
plt.xlabel("Score")
plt.ylabel("Story Title")
plt.title("Top 10 Stories by Score")
plt.gca().invert_yaxis() # highest score on top
# ----------------------------------------
# Save chart BEFORE showing
# ----------------------------------------
plt.savefig("outputs/chart1_top_stories.png")
plt.show()
# ----------------------------------------
# 3 — Chart 2: Stories per Category
# ----------------------------------------
category_counts = df["category"].value_counts()
plt.figure()
plt.bar(category_counts.index, category_counts.values)
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")
plt.savefig("outputs/chart2_categories.png")
plt.show()
plt.figure()
# ----------------------------------------
# Split data based on popularity
# ----------------------------------------
popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]
plt.scatter(popular["score"], popular["num_comments"], label="Popular")
plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")
plt.legend()
plt.savefig("outputs/chart3_scatter.png")
plt.show()
# ----------------------------------------
# Bonus — Dashboard (All charts in one figure)
# ----------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
axes[0].barh(top10["short_title"], top10["score"])
axes[0].set_title("Top 10 Stories")
axes[0].set_xlabel("Score")
axes[0].invert_yaxis()
axes[1].bar(category_counts.index, category_counts.values)
axes[1].set_title("Stories per Category")
axes[1].set_xlabel("Category")
axes[2].scatter(popular["score"], popular["num_comments"], label="Popular")
axes[2].scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
axes[2].set_title("Score vs Comments")
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Comments")
axes[2].legend()
plt.suptitle("TrendPulse Dashboard")
plt.tight_layout()
# ----------------------------------------
# Save dashboard
# ----------------------------------------
plt.savefig("outputs/dashboard.png")
plt.show()