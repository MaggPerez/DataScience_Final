import pandas as pd
import matplotlib.pyplot as plt


df_players = pd.read_csv("cleaned_csv/ACTIVE_PLAYERS_CLEANED.csv")

# Quick sanity check
print(df_players.head())
print(df_players.dtypes)


def height_to_inches(h):
    """
    Convert height like '6-6' to total inches 
    If value is missing or weird, return None.
    """
    if pd.isna(h):
        return None
    if isinstance(h, (int, float)):
        return h  # already numeric
    h = str(h)
    if "-" not in h:
        return None
    try:
        feet, inches = h.split("-")
        return int(feet) * 12 + int(inches)
    except Exception:
        return None

df_players["height_in"] = df_players["height"].apply(height_to_inches)

# Weight to numeric just in case
df_players["weight"] = pd.to_numeric(df_players["weight"], errors="coerce")

# =============== 1. HEIGHT DISTRIBUTION ===============
plt.figure()
df_players["height_in"].dropna().plot(kind="hist", bins=20)
plt.xlabel("Height (inches)")
plt.ylabel("Number of players")
plt.title("Distribution of Player Heights")
plt.tight_layout()
plt.show()

# =============== 2. WEIGHT DISTRIBUTION ===============
plt.figure()
df_players["weight"].dropna().plot(kind="hist", bins=20)
plt.xlabel("Weight (lbs)")
plt.ylabel("Number of players")
plt.title("Distribution of Player Weights")
plt.tight_layout()
plt.show()

# =============== 3. PLAYERS PER POSITION ===============
plt.figure()
df_players["position"].value_counts().plot(kind="bar")
plt.xlabel("Position")
plt.ylabel("Number of players")
plt.title("Number of Players by Position")
plt.tight_layout()
plt.show()

# =============== 4. PLAYERS PER TEAM ===============
plt.figure(figsize=(10, 5))
df_players["team.full_name"].value_counts().sort_values(ascending=False).plot(kind="bar")
plt.xlabel("Team")
plt.ylabel("Number of players")
plt.title("Number of Active Players by Team")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()


# =============== 6. AVERAGE HEIGHT BY POSITION ===============
avg_height_by_pos = (
    df_players
    .dropna(subset=["height_in"])
    .groupby("position")["height_in"]
    .mean()
    .sort_values(ascending=False)
)

plt.figure()
avg_height_by_pos.plot(kind="bar")
plt.xlabel("Position")
plt.ylabel("Average height (inches)")
plt.title("Average Height by Position")
plt.tight_layout()
plt.show()

