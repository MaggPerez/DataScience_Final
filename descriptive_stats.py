"""
Descriptive Statistical Analysis for NBA Data Science Project
Calculates and interprets key statistical measures for all datasets
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def print_section_header(title):
    """Print formatted section headers"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")

def calculate_descriptive_stats(df, numeric_cols, dataset_name):
    """
    Calculate comprehensive descriptive statistics for numeric columns

    Returns:
        DataFrame with statistics and insights dictionary
    """
    print_section_header(f"DESCRIPTIVE STATISTICS: {dataset_name}")

    stats_dict = {
        'Mean': df[numeric_cols].mean(),
        'Median': df[numeric_cols].median(),
        'Mode': df[numeric_cols].mode().iloc[0] if len(df[numeric_cols].mode()) > 0 else None,
        'Std Dev': df[numeric_cols].std(),
        'Variance': df[numeric_cols].var(),
        'Min': df[numeric_cols].min(),
        'Max': df[numeric_cols].max(),
        'Q1 (25%)': df[numeric_cols].quantile(0.25),
        'Q3 (75%)': df[numeric_cols].quantile(0.75),
        'IQR': df[numeric_cols].quantile(0.75) - df[numeric_cols].quantile(0.25)
    }

    stats_df = pd.DataFrame(stats_dict).round(2)
    print(stats_df.to_string())

    # Identify outliers for each column
    insights = {}
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        outlier_count = len(outliers)
        outlier_pct = (outlier_count / len(df)) * 100

        insights[col] = {
            'outlier_count': outlier_count,
            'outlier_pct': outlier_pct,
            'outlier_values': outliers[col].tolist()[:10]  # Show first 10
        }

        print(f"\n{col}:")
        print(f"  - Outliers detected: {outlier_count} ({outlier_pct:.1f}% of data)")
        if outlier_count > 0 and outlier_count < 20:
            print(f"  - Outlier values: {outliers[col].tolist()}")

    return stats_df, insights


def analyze_active_players():
    """Comprehensive statistical analysis of active NBA players"""
    print_section_header("ACTIVE PLAYERS ANALYSIS")

    df = pd.read_csv("cleaned_csv/ACTIVE_PLAYERS_CLEANED.csv")

    print(f"Dataset shape: {df.shape}")
    print(f"Total players: {len(df)}")

    # Convert height to inches
    def height_to_inches(h):
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

    df["height_in"] = df["height"].apply(height_to_inches)
    df["weight"] = pd.to_numeric(df["weight"], errors="coerce")

    # Numeric columns for analysis
    numeric_cols = ['height_in', 'weight']

    stats_df, insights = calculate_descriptive_stats(df, numeric_cols, "Active Players Physical Stats")

    # Position analysis
    print("\n" + "-"*80)
    print("POSITION BREAKDOWN:")
    print("-"*80)
    position_counts = df['position'].value_counts()
    print(position_counts)
    print(f"\nMost common position: {position_counts.idxmax()} ({position_counts.max()} players)")

    # Height by position
    print("\n" + "-"*80)
    print("AVERAGE HEIGHT BY POSITION:")
    print("-"*80)
    height_by_pos = df.groupby('position')['height_in'].agg(['mean', 'median', 'std', 'count']).round(2)
    print(height_by_pos.sort_values('mean', ascending=False))

    # Weight by position
    print("\n" + "-"*80)
    print("AVERAGE WEIGHT BY POSITION:")
    print("-"*80)
    weight_by_pos = df.groupby('position')['weight'].agg(['mean', 'median', 'std', 'count']).round(2)
    print(weight_by_pos.sort_values('mean', ascending=False))

    # Team distribution
    print("\n" + "-"*80)
    print("PLAYERS PER TEAM:")
    print("-"*80)
    team_counts = df['team.full_name'].value_counts()
    print(f"Average players per team: {team_counts.mean():.1f}")
    print(f"Min players: {team_counts.min()} ({team_counts.idxmin()})")
    print(f"Max players: {team_counts.max()} ({team_counts.idxmax()})")

    return df, stats_df


def analyze_team_performance():
    """Comprehensive statistical analysis of team performance metrics"""
    print_section_header("TEAM PERFORMANCE ANALYSIS")

    df = pd.read_csv("cleaned_csv/advanced_team_stats_CLEANED.csv")

    print(f"Dataset shape: {df.shape}")
    print(f"Total teams: {len(df)}")

    # Numeric columns for analysis
    numeric_cols = ['GP', 'W', 'L', 'OFF_RATING', 'DEF_RATING', 'NET_RATING']

    stats_df, insights = calculate_descriptive_stats(df, numeric_cols, "Team Performance Metrics")

    # Calculate win percentage
    df['WIN_PCT'] = (df['W'] / df['GP']).round(3)

    # Correlation analysis
    print("\n" + "-"*80)
    print("CORRELATION MATRIX: Performance Metrics vs Wins")
    print("-"*80)
    corr_cols = ['W', 'OFF_RATING', 'DEF_RATING', 'NET_RATING', 'WIN_PCT']
    correlation = df[corr_cols].corr().round(3)
    print(correlation)

    print("\n" + "-"*80)
    print("KEY CORRELATIONS WITH WINS:")
    print("-"*80)
    win_correlations = correlation['W'].sort_values(ascending=False)
    for metric, corr_value in win_correlations.items():
        if metric != 'W':
            strength = "Very Strong" if abs(corr_value) > 0.8 else "Strong" if abs(corr_value) > 0.6 else "Moderate" if abs(corr_value) > 0.4 else "Weak"
            direction = "positive" if corr_value > 0 else "negative"
            print(f"  {metric}: {corr_value:.3f} ({strength} {direction} correlation)")

    # Top performing teams
    print("\n" + "-"*80)
    print("TOP 5 TEAMS BY WINS:")
    print("-"*80)
    top_teams = df.nlargest(5, 'W')[['TEAM_NAME', 'W', 'L', 'WIN_PCT', 'NET_RATING', 'OFF_RATING', 'DEF_RATING']]
    print(top_teams.to_string(index=False))

    # Bottom performing teams
    print("\n" + "-"*80)
    print("BOTTOM 5 TEAMS BY WINS:")
    print("-"*80)
    bottom_teams = df.nsmallest(5, 'W')[['TEAM_NAME', 'W', 'L', 'WIN_PCT', 'NET_RATING', 'OFF_RATING', 'DEF_RATING']]
    print(bottom_teams.to_string(index=False))

    return df, stats_df, correlation


def analyze_jokic_career():
    """Statistical analysis of Nikola Jokic career progression"""
    print_section_header("NIKOLA JOKIC CAREER ANALYSIS")

    df = pd.read_csv("cleaned_csv/Nikola_Jokic_Info_CLEANED.csv")

    print(f"Dataset shape: {df.shape}")
    print(f"Seasons played: {len(df)}")

    # Numeric columns for analysis
    numeric_cols = ['GP', 'GS', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A',
                    'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'REB', 'AST', 'STL', 'BLK',
                    'TOV', 'PF', 'PTS']

    # Only use columns that exist
    numeric_cols = [col for col in numeric_cols if col in df.columns]

    stats_df, insights = calculate_descriptive_stats(df, numeric_cols, "Jokic Career Statistics")

    # Career progression analysis
    print("\n" + "-"*80)
    print("CAREER PROGRESSION (Key Stats):")
    print("-"*80)
    progression = df[['SEASON_ID', 'GP', 'MIN', 'PTS', 'REB', 'AST', 'FG_PCT']].round(2)
    print(progression.to_string(index=False))

    # Career averages
    print("\n" + "-"*80)
    print("CAREER AVERAGES:")
    print("-"*80)
    print(f"Points per season: {df['PTS'].mean():.1f}")
    print(f"Rebounds per season: {df['REB'].mean():.1f}")
    print(f"Assists per season: {df['AST'].mean():.1f}")
    print(f"Games played per season: {df['GP'].mean():.1f}")

    # Best season
    best_season_pts = df.loc[df['PTS'].idxmax()]
    print("\n" + "-"*80)
    print(f"BEST SEASON (by points): {best_season_pts['SEASON_ID']}")
    print("-"*80)
    print(f"Points: {best_season_pts['PTS']:.0f}")
    print(f"Rebounds: {best_season_pts['REB']:.0f}")
    print(f"Assists: {best_season_pts['AST']:.0f}")

    return df, stats_df


def create_correlation_heatmap(df, columns, title, filename):
    """Create and save correlation heatmap"""
    plt.figure(figsize=(10, 8))
    correlation = df[columns].corr()

    sns.heatmap(correlation, annot=True, fmt='.2f', cmap='coolwarm',
                center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8})

    plt.title(title, fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(f'visualizations/{filename}', dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved correlation heatmap: visualizations/{filename}")
    plt.close()


def create_boxplots():
    """Create boxplot visualizations for distribution comparison"""
    print_section_header("CREATING BOXPLOT VISUALIZATIONS")

    # Active players boxplots
    df_players = pd.read_csv("cleaned_csv/ACTIVE_PLAYERS_CLEANED.csv")

    def height_to_inches(h):
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

    df_players["height_in"] = df_players["height"].apply(height_to_inches)
    df_players["weight"] = pd.to_numeric(df_players["weight"], errors="coerce")

    # Height by position boxplot
    plt.figure(figsize=(12, 6))
    df_players_clean = df_players.dropna(subset=['height_in', 'position'])
    positions_order = df_players_clean.groupby('position')['height_in'].median().sort_values(ascending=False).index

    sns.boxplot(data=df_players_clean, x='position', y='height_in', order=positions_order, palette='Set2')
    plt.title('Height Distribution by Position', fontsize=14, fontweight='bold')
    plt.xlabel('Position', fontsize=12)
    plt.ylabel('Height (inches)', fontsize=12)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('visualizations/height_by_position_boxplot.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: visualizations/height_by_position_boxplot.png")
    plt.close()

    # Weight by position boxplot
    plt.figure(figsize=(12, 6))
    df_players_clean = df_players.dropna(subset=['weight', 'position'])

    sns.boxplot(data=df_players_clean, x='position', y='weight', order=positions_order, palette='Set3')
    plt.title('Weight Distribution by Position', fontsize=14, fontweight='bold')
    plt.xlabel('Position', fontsize=12)
    plt.ylabel('Weight (lbs)', fontsize=12)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('visualizations/weight_by_position_boxplot.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: visualizations/weight_by_position_boxplot.png")
    plt.close()


def main():
    """Run all statistical analyses"""
    import os
    os.makedirs('visualizations', exist_ok=True)

    print("\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█" + "  NBA DATA SCIENCE PROJECT - COMPREHENSIVE STATISTICAL ANALYSIS".center(78) + "█")
    print("█" + " "*78 + "█")
    print("█"*80)

    # Analyze all datasets
    df_players, stats_players = analyze_active_players()
    df_teams, stats_teams, correlation = analyze_team_performance()
    df_jokic, stats_jokic = analyze_jokic_career()

    # Create correlation heatmaps
    print_section_header("GENERATING CORRELATION HEATMAPS")

    # Team performance correlation heatmap
    team_corr_cols = ['W', 'L', 'OFF_RATING', 'DEF_RATING', 'NET_RATING']
    create_correlation_heatmap(df_teams, team_corr_cols,
                              'Team Performance Metrics Correlation Matrix',
                              'team_correlation_heatmap.png')

    # Player physical stats correlation
    player_corr_cols = ['height_in', 'weight']
    df_players_clean = df_players[player_corr_cols].dropna()
    if len(df_players_clean) > 0:
        create_correlation_heatmap(df_players_clean, player_corr_cols,
                                  'Player Physical Attributes Correlation',
                                  'player_correlation_heatmap.png')

    # Create boxplots
    create_boxplots()

    print("\n" + "█"*80)
    print("█" + "  ANALYSIS COMPLETE - All statistics calculated and visualizations saved".center(78) + "█")
    print("█"*80 + "\n")


if __name__ == "__main__":
    main()
