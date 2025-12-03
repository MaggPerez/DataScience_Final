import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("cleaned_csv/advanced_team_stats_CLEANED.csv")

# Good defense win more?
plt.figure(figsize=(10,6))
plt.scatter(df["OFF_RATING"], df["W"], s=70)
plt.xlabel("Offensive Rating")
plt.ylabel("Wins")
plt.title("Do Teams With Better Offenses Win More?")
plt.grid(True)
plt.show()

# Is defense more important than offense?
plt.figure(figsize=(10,6))
plt.scatter(df["DEF_RATING"], df["W"], s=70, color="orange")
plt.xlabel("Defensive Rating (lower is better)")
plt.ylabel("Wins")
plt.title("Does Better Defense Predict More Wins?")
plt.grid(True)
plt.show()

# Win percentage vs Net Rating
df["WIN_PCT"] = df["W"] / df["GP"]

plt.figure(figsize=(10,6))
plt.scatter(df["NET_RATING"], df["WIN_PCT"], s=80, color="green")
plt.xlabel("Net Rating")
plt.ylabel("Win Percentage")
plt.title("Net Rating vs Win% (Strongest Predictor of Team Success)")
plt.grid(True)
plt.show()


# Bar chart of wins by team
df_sorted = df.sort_values("W", ascending=False)

plt.figure(figsize=(12,6))
plt.bar(df_sorted["TEAM_NAME"], df_sorted["W"])
plt.xticks(rotation=90)
plt.ylabel("Wins")
plt.title("Wins by Team")
plt.tight_layout()
plt.show()



