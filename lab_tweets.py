import json
import glob
import matplotlib.pyplot as plt
import os


# ----------------------
# load all tweet files
# ----------------------
tweets = []

files = sorted(glob.glob("trump_tweet_data_archive-master/master_*.json"))

for filename in files:
    print(f"Loading: {filename}")
    with open(filename, "r", encoding="utf8") as f:
        data = json.load(f)

        if isinstance(data, list):
            tweets.extend(data)

        elif isinstance(data, dict):
            if "tweets" in data:
                tweets.extend(data["tweets"])
            elif "data" in data:
                tweets.extend(data["data"])
            else:
                tweets.append(data)

total = len(tweets)
print("len(tweets) =", total)

# ----------------------
# phrases to count
# ----------------------
phrases = [
    "obama",
    "trump",
    "mexico",
    "russia",
    "fake news",
    "mainstream media",
    "daca",
    "wall"
]


# ----------------------
# count occurrences
# ----------------------
counts = {p: 0 for p in phrases}

for tweet in tweets:
    text = str(tweet.get("text", "")).lower()
    for phrase in phrases:
        if phrase in text:
            counts[phrase] += 1

print("counts=", counts)


# ----------------------
# compute percentages
# ----------------------
total = len(tweets)
percents = {p: counts[p] / total * 100 for p in phrases}


# ----------------------
# markdown table output
# ----------------------
print("\n| phrase            | percent of tweets |")
print("| ----------------- | ----------------- |")

for phrase in sorted(phrases):
    print(f"| {phrase:>17} | {percents[phrase]:06.2f}             |")             


# ----------------------
# bar chart
# ----------------------
labels = list(percents.keys())
values = list(percents.values())

plt.bar(labels, values)
plt.xticks(rotation=45, ha="right")
plt.ylabel("Percent of Tweets")
plt.title("Keyword Frequency in Tweets")
plt.tight_layout()
plt.savefig("plot.png")
plt.show()
