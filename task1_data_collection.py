import requests # used to make API calls

import time   # used to add delay between requests

import os    # used to create folders

import json   # used to save data in JSON format

from datetime import datetime # used to get current timestamp
# ----------------------------------------
# Define simple keyword-based categories
# ----------------------------------------
# Each category contains keywords to match against story titles
categories = {

  "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],

  "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],

  "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],

  "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],

  "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]

}
# ----------------------------------------
# Function to assign category based on title
# ----------------------------------------
def get_category(title):
  title = title.lower() # convert title to lowercase for matching
  for category, keywords in categories.items(): # loop through each category
    for word in keywords: # check each keyword
      if word in title: # if keyword is found in title
        return category # return that category
  return None # return None if no keyword matches
# ----------------------------------------
# Fetch top story IDs from Hacker News API
# ----------------------------------------
url = "https://hacker-news.firebaseio.com/v0/topstories.json"
# Header helps identify your script
headers = {"User-Agent": "TrendPulse/1.0"}
# Make request to get top story IDs
response = requests.get(url, headers=headers)
response.raise_for_status() # raise error if request fails
# Take first 500 story IDs
story_ids = response.json()[:500]
# ----------------------------------------
# Initialize storage variables
# ----------------------------------------
collected = [] # list to store final collected stories
# Track how many stories collected per category
category_count = {key: 0 for key in categories}
target = 25 # maximum stories per category
# ----------------------------------------
# Loop through each story ID
# ----------------------------------------
for story_id in story_ids:
  if sum(category_count.values()) >= 125:
    break
  # Construct API URL for individual story
  story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
  try:
    # Fetch story details
    res = requests.get(story_url, headers=headers)
    res.raise_for_status()
  except requests.RequestException:
    # If request fails, skip this story
    print(f"Failed to fetch story {story_id}")
    continue
  # Convert response to JSON
  story = res.json()
  if not story or "title" not in story:
    continue
  title = story["title"]
  # Get category based on title keywords
  category = get_category(title)
  # ----------------------------------------
  # Filter stories
  # ----------------------------------------
  # Keep only:
  # 1. Stories that match a category
  # 2. Category count is still below target
  if category and category_count[category] < target:
    # Extract required fields
    data = {
      "post_id": story.get("id"),
      "title": title,
      "category": category,
      "score": story.get("score", 0),
      "num_comments": story.get("descendants", 0),
      "author": story.get("by"),
      "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
 # Add story to collected list
    collected.append(data)
    # Increment category count
    category_count[category] += 1
    print(f"[{category.upper()}] {title}")
    # Delay to avoid hitting API rate limits
    time.sleep(1.5)
# ----------------------------------------
# Save results to JSON file
# ----------------------------------------
# Create "data" folder if it doesn't exist
os.makedirs("data", exist_ok=True)
# Generate filename with current date
filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"
# Write collected data into JSON file
with open(filename, "w") as f:
  json.dump(collected, f, indent=4)
# ----------------------------------------
# Final output summary
# ----------------------------------------
print(f"\n Collected {len(collected)} stories across categories.")
print(f"Saved to {filename}")