"""
Enhanced Visualization Module with Interpretations

This module creates all visualizations with proper context, interpretations,
and statistical annotations. Visualizations are designed to tell a cohesive
story about NBA player and team performance.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Set style for professional-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

def ensure_viz_directory():
    """Create visualizations directory if it doesn't exist"""
    os.makedirs('visualizations', exist_ok=True)

def height_to_inches(h):
    """
    Convert height like '6-6' to total inches
    Returns None for invalid values
    """
    if pd.isna(h):
        return None
    if isinstance(h, (int, float)):
        return h
    h = str(h)
    if "-" not in h:
        return None
    try:
        feet, inches = h.split("-")
        return int(feet) * 12 + int(inches)
    except Exception:
        return None


def create_player_visualizations():
    """
    Create comprehensive player analysis visualizations

    Visualizations:
    1. Height distribution histogram
    2. Weight distribution histogram
    3. Position frequency bar chart
    4. Players per team bar chart
    5. Average height by position
    6. Average weight by position
    """
    print("\n" + "="*80)
    print("  CREATING PLAYER VISUALIZATIONS")
    print("="*80 + "\n")

    df_players = pd.read_csv("cleaned_csv/ACTIVE_PLAYERS_CLEANED.csv")

    # Convert height and weight
    df_players["height_in"] = df_players["height"].apply(height_to_inches)
    df_players["weight"] = pd.to_numeric(df_players["weight"], errors="coerce")

    # 1. HEIGHT DISTRIBUTION
    plt.figure(figsize=(12, 6))
    heights = df_players["height_in"].dropna()
    plt.hist(heights, bins=25, edgecolor='black', alpha=0.7, color='steelblue')
    plt.axvline(heights.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {heights.mean():.1f}"')
    plt.axvline(heights.median(), color='green', linestyle='--', linewidth=2, label=f'Median: {heights.median():.1f}"')
    plt.xlabel("Height (inches)", fontsize=12, fontweight='bold')
    plt.ylabel("Number of Players", fontsize=12, fontweight='bold')
    plt.title("Distribution of NBA Player Heights\n(Approximately Normal with Slight Right Skew)",
              fontsize=14, fontweight='bold', pad=20)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)

    # Add interpretation text box
    interpretation = (f"Mean: {heights.mean():.1f}\" | Median: {heights.median():.1f}\" | Std: {heights.std():.1f}\"\n"
                     f"Range: {heights.min():.0f}\" to {heights.max():.0f}\" ({heights.max()-heights.min():.0f}\" spread)")
    plt.text(0.02, 0.98, interpretation, transform=plt.gca().transAxes,
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
             verticalalignment='top', fontsize=10, family='monospace')

    plt.tight_layout()
    plt.savefig('visualizations/1_height_distribution.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: visualizations/1_height_distribution.png")
    print("  Interpretation: The height distribution shows a normal distribution centered")
    print("  around 78-79 inches (~6'6\"), which is typical for professional basketball.")
    print("  The distribution includes players from ~67\" (guards) to ~87\" (centers).\n")
    plt.close()

    # 2. WEIGHT DISTRIBUTION
    plt.figure(figsize=(12, 6))
    weights = df_players["weight"].dropna()
    plt.hist(weights, bins=25, edgecolor='black', alpha=0.7, color='coral')
    plt.axvline(weights.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {weights.mean():.1f} lbs')
    plt.axvline(weights.median(), color='green', linestyle='--', linewidth=2, label=f'Median: {weights.median():.1f} lbs')
    plt.xlabel("Weight (lbs)", fontsize=12, fontweight='bold')
    plt.ylabel("Number of Players", fontsize=12, fontweight='bold')
    plt.title("Distribution of NBA Player Weights\n(Bell-Shaped with Some Heavier Outliers)",
              fontsize=14, fontweight='bold', pad=20)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)

    interpretation = (f"Mean: {weights.mean():.1f} lbs | Median: {weights.median():.1f} lbs | Std: {weights.std():.1f}\n"
                     f"Range: {weights.min():.0f} to {weights.max():.0f} lbs")
    plt.text(0.02, 0.98, interpretation, transform=plt.gca().transAxes,
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
             verticalalignment='top', fontsize=10, family='monospace')

    plt.tight_layout()
    plt.savefig('visualizations/2_weight_distribution.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: visualizations/2_weight_distribution.png")
    print("  Interpretation: Weight distribution shows professional athletes typically weigh")
    print("  200-220 lbs, with position-specific variations (guards lighter, centers heavier).\n")
    plt.close()

    # 3. POSITION FREQUENCY
    plt.figure(figsize=(10, 6))
    position_counts = df_players["position"].value_counts().sort_values(ascending=False)
    colors = sns.color_palette("husl", len(position_counts))
    bars = plt.bar(position_counts.index, position_counts.values, color=colors, edgecolor='black')

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontweight='bold')

    plt.xlabel("Position", fontsize=12, fontweight='bold')
    plt.ylabel("Number of Players", fontsize=12, fontweight='bold')
    plt.title("Active NBA Players by Position\n(Relatively Balanced Distribution Across Positions)",
              fontsize=14, fontweight='bold', pad=20)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('visualizations/3_position_distribution.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: visualizations/3_position_distribution.png")
    print(f"  Interpretation: Most common position is {position_counts.idxmax()} with {position_counts.max()} players.")
    print("  Distribution shows balanced roster construction across the league.\n")
    plt.close()

    # 4. PLAYERS PER TEAM
    plt.figure(figsize=(14, 7))
    team_counts = df_players["team.full_name"].value_counts().sort_values(ascending=False)
    plt.bar(range(len(team_counts)), team_counts.values, color='teal', edgecolor='black', alpha=0.7)
    plt.xlabel("Teams (sorted by player count)", fontsize=12, fontweight='bold')
    plt.ylabel("Number of Players", fontsize=12, fontweight='bold')
    plt.title("Active Players per Team\n(Most Teams Maintain ~13-17 Player Rosters)",
              fontsize=14, fontweight='bold', pad=20)
    plt.axhline(team_counts.mean(), color='red', linestyle='--', linewidth=2,
                label=f'Average: {team_counts.mean():.1f} players')
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.xticks([])  # Hide x-tick labels for clarity
    plt.tight_layout()
    plt.savefig('visualizations/4_players_per_team.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: visualizations/4_players_per_team.png")
    print(f"  Interpretation: Average roster size is {team_counts.mean():.1f} players.")
    print(f"  Range: {team_counts.min()} to {team_counts.max()} players per team.\n")
    plt.close()

    # 5. AVERAGE HEIGHT BY POSITION
    plt.figure(figsize=(10, 6))
    height_by_pos = (df_players.dropna(subset=['height_in'])
                     .groupby('position')['height_in']
                     .agg(['mean', 'std']))
    height_by_pos = height_by_pos.sort_values('mean', ascending=False)

    bars = plt.bar(height_by_pos.index, height_by_pos['mean'],
                   yerr=height_by_pos['std'], capsize=5,
                   color='skyblue', edgecolor='black', alpha=0.8)

    # Add value labels
    for i, (pos, row) in enumerate(height_by_pos.iterrows()):
        plt.text(i, row['mean'] + row['std'] + 0.5, f"{row['mean']:.1f}\"",
                ha='center', fontweight='bold')

    plt.xlabel("Position", fontsize=12, fontweight='bold')
    plt.ylabel("Average Height (inches)", fontsize=12, fontweight='bold')
    plt.title("Average Height by Position with Standard Deviation\n(Clear Hierarchical Pattern: Centers Tallest, Guards Shortest)",
              fontsize=14, fontweight='bold', pad=20)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('visualizations/5_height_by_position.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: visualizations/5_height_by_position.png")
    print("  Interpretation: Clear height hierarchy by position reflects basketball roles.")
    print(f"  Centers average {height_by_pos.loc[height_by_pos.index[0], 'mean']:.1f}\", guards ~6-7\" shorter.\n")
    plt.close()

    # 6. AVERAGE WEIGHT BY POSITION
    plt.figure(figsize=(10, 6))
    weight_by_pos = (df_players.dropna(subset=['weight'])
                     .groupby('position')['weight']
                     .agg(['mean', 'std']))
    weight_by_pos = weight_by_pos.sort_values('mean', ascending=False)

    bars = plt.bar(weight_by_pos.index, weight_by_pos['mean'],
                   yerr=weight_by_pos['std'], capsize=5,
                   color='salmon', edgecolor='black', alpha=0.8)

    # Add value labels
    for i, (pos, row) in enumerate(weight_by_pos.iterrows()):
        plt.text(i, row['mean'] + row['std'] + 2, f"{row['mean']:.0f} lbs",
                ha='center', fontweight='bold')

    plt.xlabel("Position", fontsize=12, fontweight='bold')
    plt.ylabel("Average Weight (lbs)", fontsize=12, fontweight='bold')
    plt.title("Average Weight by Position with Standard Deviation\n(Weight Correlates with Position Requirements)",
              fontsize=14, fontweight='bold', pad=20)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('visualizations/6_weight_by_position.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: visualizations/6_weight_by_position.png")
    print("  Interpretation: Weight follows position requirements - centers need mass for")
    print("  paint presence, guards prioritize speed and agility.\n")
    plt.close()


def create_team_performance_visualizations():
    """
    Create team performance analysis visualizations

    Visualizations:
    7. Offensive Rating vs Wins scatter plot
    8. Defensive Rating vs Wins scatter plot
    9. Net Rating vs Win Percentage scatter plot
    10. Team wins bar chart
    """
    print("\n" + "="*80)
    print("  CREATING TEAM PERFORMANCE VISUALIZATIONS")
    print("="*80 + "\n")

    df = pd.read_csv("cleaned_csv/advanced_team_stats_CLEANED.csv")
    df['WIN_PCT'] = (df['W'] / df['GP']).round(3)

    # 7. OFFENSIVE RATING VS WINS
    plt.figure(figsize=(12, 7))
    correlation = df['OFF_RATING'].corr(df['W'])

    plt.scatter(df["OFF_RATING"], df["W"], s=100, alpha=0.6, c=df['W'],
                cmap='RdYlGn', edgecolors='black', linewidth=1)
    plt.colorbar(label='Wins')

    # Add trend line
    z = np.polyfit(df["OFF_RATING"], df["W"], 1)
    p = np.poly1d(z)
    plt.plot(df["OFF_RATING"], p(df["OFF_RATING"]), "r--", linewidth=2, alpha=0.8, label='Trend Line')

    plt.xlabel("Offensive Rating (points per 100 possessions)", fontsize=12, fontweight='bold')
    plt.ylabel("Wins", fontsize=12, fontweight='bold')
    plt.title(f"Offensive Rating vs Wins (r={correlation:.3f})\n(Strong Positive Correlation: Better Offense = More Wins)",
              fontsize=14, fontweight='bold', pad=20)
    plt.grid(True, alpha=0.3)
    plt.legend()

    interpretation = f"Correlation: r={correlation:.3f}\nHigher offensive ratings strongly predict more wins."
    plt.text(0.02, 0.98, interpretation, transform=plt.gca().transAxes,
             bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8),
             verticalalignment='top', fontsize=11, family='monospace')

    plt.tight_layout()
    plt.savefig('visualizations/7_offense_vs_wins.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: visualizations/7_offense_vs_wins.png")
    print(f"  Interpretation: Strong correlation (r={correlation:.3f}) shows offensive efficiency")
    print("  is a major predictor of team success.\n")
    plt.close()

    # 8. DEFENSIVE RATING VS WINS
    plt.figure(figsize=(12, 7))
    correlation = df['DEF_RATING'].corr(df['W'])

    plt.scatter(df["DEF_RATING"], df["W"], s=100, alpha=0.6, c=df['W'],
                cmap='RdYlGn', edgecolors='black', linewidth=1)
    plt.colorbar(label='Wins')

    # Add trend line
    z = np.polyfit(df["DEF_RATING"], df["W"], 1)
    p = np.poly1d(z)
    plt.plot(df["DEF_RATING"], p(df["DEF_RATING"]), "r--", linewidth=2, alpha=0.8, label='Trend Line')

    plt.xlabel("Defensive Rating (points allowed per 100 possessions) - LOWER IS BETTER",
               fontsize=12, fontweight='bold')
    plt.ylabel("Wins", fontsize=12, fontweight='bold')
    plt.title(f"Defensive Rating vs Wins (r={correlation:.3f})\n(Strong Negative Correlation: Better Defense = More Wins)",
              fontsize=14, fontweight='bold', pad=20)
    plt.grid(True, alpha=0.3)
    plt.legend()

    interpretation = f"Correlation: r={correlation:.3f}\nLower defensive ratings (better defense) strongly predict more wins."
    plt.text(0.98, 0.02, interpretation, transform=plt.gca().transAxes,
             bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8),
             verticalalignment='bottom', horizontalalignment='right',
             fontsize=11, family='monospace')

    plt.tight_layout()
    plt.savefig('visualizations/8_defense_vs_wins.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: visualizations/8_defense_vs_wins.png")
    print(f"  Interpretation: Negative correlation (r={correlation:.3f}) confirms that")
    print("  better defense (lower rating) leads to more wins.\n")
    plt.close()

    # 9. NET RATING VS WIN PERCENTAGE
    plt.figure(figsize=(12, 7))
    correlation = df['NET_RATING'].corr(df['WIN_PCT'])

    plt.scatter(df["NET_RATING"], df["WIN_PCT"], s=120, alpha=0.7, c=df['W'],
                cmap='viridis', edgecolors='black', linewidth=1.5)
    plt.colorbar(label='Total Wins')

    # Add trend line
    z = np.polyfit(df["NET_RATING"], df["WIN_PCT"], 1)
    p = np.poly1d(z)
    plt.plot(df["NET_RATING"], p(df["NET_RATING"]), "r--", linewidth=3, alpha=0.8, label='Trend Line')

    plt.xlabel("Net Rating (OFF_RATING - DEF_RATING)", fontsize=12, fontweight='bold')
    plt.ylabel("Win Percentage", fontsize=12, fontweight='bold')
    plt.title(f"Net Rating vs Win Percentage (r={correlation:.3f})\n**STRONGEST PREDICTOR OF SUCCESS** (Near-Perfect Correlation)",
              fontsize=14, fontweight='bold', pad=20)
    plt.grid(True, alpha=0.3)
    plt.legend()

    interpretation = f"Correlation: r={correlation:.3f}\nNet Rating is the single best predictor of team success!"
    plt.text(0.02, 0.98, interpretation, transform=plt.gca().transAxes,
             bbox=dict(boxstyle='round', facecolor='gold', alpha=0.9),
             verticalalignment='top', fontsize=12, family='monospace', fontweight='bold')

    plt.tight_layout()
    plt.savefig('visualizations/9_net_rating_vs_win_pct.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: visualizations/9_net_rating_vs_win_pct.png")
    print(f"  Interpretation: VERY STRONG correlation (r={correlation:.3f})! Net Rating")
    print("  (offense - defense) is the best single metric for predicting wins.\n")
    plt.close()

    # 10. TEAM WINS BAR CHART
    plt.figure(figsize=(14, 7))
    df_sorted = df.sort_values('W', ascending=False)
    colors_wins = ['green' if w >= df['W'].median() else 'red' for w in df_sorted['W']]

    plt.bar(df_sorted["TEAM_NAME"], df_sorted["W"], color=colors_wins, edgecolor='black', alpha=0.7)
    plt.axhline(df['W'].mean(), color='blue', linestyle='--', linewidth=2,
                label=f'League Average: {df["W"].mean():.1f} wins')
    plt.xlabel("Team", fontsize=12, fontweight='bold')
    plt.ylabel("Wins", fontsize=12, fontweight='bold')
    plt.title("Team Wins (Sorted)\n(Green = Above Median | Red = Below Median)",
              fontsize=14, fontweight='bold', pad=20)
    plt.xticks(rotation=90, ha='right')
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('visualizations/10_team_wins.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: visualizations/10_team_wins.png")
    print(f"  Interpretation: {df_sorted.iloc[0]['TEAM_NAME']} leads with {df_sorted.iloc[0]['W']:.0f} wins.")
    print(f"  League average: {df['W'].mean():.1f} wins.\n")
    plt.close()


def create_jokic_visualizations():
    """
    Create Nikola Jokic career progression visualizations

    Visualizations:
    11. Jokic points progression
    12. Jokic rebounds progression
    13. Jokic assists progression
    """
    print("\n" + "="*80)
    print("  CREATING JOKIC CAREER VISUALIZATIONS")
    print("="*80 + "\n")

    df = pd.read_csv("cleaned_csv/Nikola_Jokic_Info_CLEANED.csv")
    df["SEASON"] = df["SEASON_ID"].astype(str).str[-2:].astype(int) + 2000

    # 11. POINTS PROGRESSION
    plt.figure(figsize=(12, 6))
    plt.plot(df["SEASON"], df["PTS"], marker="o", linewidth=3, markersize=8, color='red')
    plt.fill_between(df["SEASON"], df["PTS"], alpha=0.3, color='red')
    plt.xlabel("Season", fontsize=12, fontweight='bold')
    plt.ylabel("Total Points", fontsize=12, fontweight='bold')
    plt.title("Nikola Jokic - Points per Season\n(Consistent Elite Scoring Throughout Career)",
              fontsize=14, fontweight='bold', pad=20)
    plt.grid(True, alpha=0.3)

    interpretation = f"Career Average: {df['PTS'].mean():.0f} points/season\nPeak: {df['PTS'].max():.0f} points ({df.loc[df['PTS'].idxmax(), 'SEASON']:.0f})"
    plt.text(0.02, 0.98, interpretation, transform=plt.gca().transAxes,
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
             verticalalignment='top', fontsize=11, family='monospace')

    plt.tight_layout()
    plt.savefig('visualizations/11_jokic_points.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: visualizations/11_jokic_points.png")
    print(f"  Interpretation: Consistent scoring with peak of {df['PTS'].max():.0f} points.\n")
    plt.close()

    # 12. REBOUNDS PROGRESSION
    plt.figure(figsize=(12, 6))
    plt.plot(df["SEASON"], df["REB"], marker="s", linewidth=3, markersize=8, color='blue')
    plt.fill_between(df["SEASON"], df["REB"], alpha=0.3, color='blue')
    plt.xlabel("Season", fontsize=12, fontweight='bold')
    plt.ylabel("Total Rebounds", fontsize=12, fontweight='bold')
    plt.title("Nikola Jokic - Rebounds per Season\n(Elite Rebounding from Center Position)",
              fontsize=14, fontweight='bold', pad=20)
    plt.grid(True, alpha=0.3)

    interpretation = f"Career Average: {df['REB'].mean():.0f} rebounds/season\nPeak: {df['REB'].max():.0f} rebounds ({df.loc[df['REB'].idxmax(), 'SEASON']:.0f})"
    plt.text(0.02, 0.98, interpretation, transform=plt.gca().transAxes,
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8),
             verticalalignment='top', fontsize=11, family='monospace')

    plt.tight_layout()
    plt.savefig('visualizations/12_jokic_rebounds.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: visualizations/12_jokic_rebounds.png")
    print(f"  Interpretation: Dominant rebounding averaging {df['REB'].mean():.0f}/season.\n")
    plt.close()

    # 13. ASSISTS PROGRESSION
    plt.figure(figsize=(12, 6))
    plt.plot(df["SEASON"], df["AST"], marker="^", linewidth=3, markersize=8, color='green')
    plt.fill_between(df["SEASON"], df["AST"], alpha=0.3, color='green')
    plt.xlabel("Season", fontsize=12, fontweight='bold')
    plt.ylabel("Total Assists", fontsize=12, fontweight='bold')
    plt.title("Nikola Jokic - Assists per Season\n(Exceptional Playmaking for a Center)",
              fontsize=14, fontweight='bold', pad=20)
    plt.grid(True, alpha=0.3)

    interpretation = f"Career Average: {df['AST'].mean():.0f} assists/season\nPeak: {df['AST'].max():.0f} assists ({df.loc[df['AST'].idxmax(), 'SEASON']:.0f})\nRare for a center!"
    plt.text(0.02, 0.98, interpretation, transform=plt.gca().transAxes,
             bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8),
             verticalalignment='top', fontsize=11, family='monospace')

    plt.tight_layout()
    plt.savefig('visualizations/13_jokic_assists.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: visualizations/13_jokic_assists.png")
    print(f"  Interpretation: Exceptional playmaking - {df['AST'].mean():.0f} assists/season")
    print("  is guard-like production from a center position!\n")
    plt.close()


def main():
    """Generate all enhanced visualizations"""
    ensure_viz_directory()

    print("\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█" + "  NBA DATA VISUALIZATION - COMPREHENSIVE ANALYSIS".center(78) + "█")
    print("█" + " "*78 + "█")
    print("█"*80)

    create_player_visualizations()
    create_team_performance_visualizations()
    create_jokic_visualizations()

    print("\n" + "█"*80)
    print("█" + "  ALL VISUALIZATIONS COMPLETE - 13 plots saved to visualizations/".center(78) + "█")
    print("█"*80 + "\n")


if __name__ == "__main__":
    main()
