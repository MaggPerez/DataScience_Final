"""
Descriptive Statistical Analysis for NBA Data Science Project
Calculates and interprets key statistical measures for all datasets
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


"""
Calculate comprehensive descriptive statistics for numeric columns
Returns: DataFrame with statistics and insights dictionary
"""
def calculate_descriptive_stats(df, numeric_cols, dataset_name):
    
    # Calculate descriptive statistics
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
    
    # Create DataFrame from stats_dict
    stats_df = pd.DataFrame(stats_dict).round(2)


    # Identify outliers for each column
    insights = {}
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Find outliers
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        outlier_count = len(outliers)
        outlier_pct = (outlier_count / len(df)) * 100
        
        
        # Store insights
        insights[col] = {
            'outlier_count': outlier_count,
            'outlier_pct': outlier_pct,
            'outlier_values': outliers[col].tolist()[:10]  # Show first 10
        }
        
    # return stats DataFrame and insights
    return stats_df, insights


"""
Comprehensive statistical analysis of active NBA players
"""
def analyze_active_players():
    
    # Load cleaned active players data
    df = pd.read_csv("cleaned_csv/ACTIVE_PLAYERS_CLEANED.csv")


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
        
        
        
    # Add height in inches column
    df["height_in"] = df["height"].apply(height_to_inches)
    df["weight"] = pd.to_numeric(df["weight"], errors="coerce")

    # Numeric columns for analysis
    numeric_cols = ['height_in', 'weight']
    
    
    # Calculate descriptive statistics
    stats_df, insights = calculate_descriptive_stats(df, numeric_cols, "Active Players Physical Stats")

    return df, stats_df





"""
Comprehensive statistical analysis of team performance metrics
"""
def analyze_team_performance():
    
    # Load cleaned team performance data
    df = pd.read_csv("cleaned_csv/advanced_team_stats_CLEANED.csv")


    # Numeric columns for analysis
    numeric_cols = ['GP', 'W', 'L', 'OFF_RATING', 'DEF_RATING', 'NET_RATING']


    # Calculate descriptive statistics
    stats_df, insights = calculate_descriptive_stats(df, numeric_cols, "Team Performance Metrics")



    # Calculate win percentage
    df['WIN_PCT'] = (df['W'] / df['GP']).round(3)


    # Correlation analysis
    corr_cols = ['W', 'OFF_RATING', 'DEF_RATING', 'NET_RATING', 'WIN_PCT']
    correlation = df[corr_cols].corr().round(3)



    # returns dataframe, stats dataframe, and correlation matrix
    return df, stats_df, correlation



"""
Statistical analysis of Nikola Jokic career progression
"""
def analyze_jokic_career():
    
    # Load cleaned Nikola Jokic career data
    df = pd.read_csv("cleaned_csv/Nikola_Jokic_Info_CLEANED.csv")

    # Numeric columns for analysis
    numeric_cols = ['GP', 'GS', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A',
                    'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'REB', 'AST', 'STL', 'BLK',
                    'TOV', 'PF', 'PTS']



    # Only use columns that exist
    numeric_cols = [col for col in numeric_cols if col in df.columns]

    
    # Calculate descriptive statistics
    stats_df, insights = calculate_descriptive_stats(df, numeric_cols, "Jokic Career Statistics")

    return df, stats_df


"""
Create and save correlation heatmap
"""
def create_correlation_heatmap(df, columns, title, filename):
    
    # Create correlation heatmap
    plt.figure(figsize=(10, 8))
    correlation = df[columns].corr()
    
    
    
    # Plot heatmap
    sns.heatmap(correlation, annot=True, fmt='.2f', cmap='coolwarm',
                center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8})

    plt.title(title, fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    
    plt.savefig(f'visualizations/{filename}', dpi=300, bbox_inches='tight')
    print(f"✓ Saved correlation heatmap: visualizations/{filename}")
    
    plt.close()



"""
Create boxplot visualizations for distribution comparison
"""
def create_boxplots():

    # Active players boxplots
    df_players = pd.read_csv("cleaned_csv/ACTIVE_PLAYERS_CLEANED.csv")
    
    
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



    # Add height in inches column
    df_players["height_in"] = df_players["height"].apply(height_to_inches)
    df_players["weight"] = pd.to_numeric(df_players["weight"], errors="coerce")

    # Height by position boxplot
    plt.figure(figsize=(12, 6))
    df_players_clean = df_players.dropna(subset=['height_in', 'position'])
    positions_order = df_players_clean.groupby('position')['height_in'].median().sort_values(ascending=False).index



    # Create boxplot of player heights by position
    sns.boxplot(data=df_players_clean, x='position', y='height_in', order=positions_order, palette='Set2')
    plt.title('Height Distribution by Position', fontsize=14, fontweight='bold')
    plt.xlabel('Position', fontsize=12)
    plt.ylabel('Height (inches)', fontsize=12)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    
    
    # saving the figure
    plt.savefig('visualizations/height_by_position_boxplot.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: visualizations/height_by_position_boxplot.png")
    plt.close()


    # Weight by position boxplot
    plt.figure(figsize=(12, 6))
    df_players_clean = df_players.dropna(subset=['weight', 'position'])


    # Create boxplot of player weights by position
    sns.boxplot(data=df_players_clean, x='position', y='weight', order=positions_order, palette='Set3')
    plt.title('Weight Distribution by Position', fontsize=14, fontweight='bold')
    plt.xlabel('Position', fontsize=12)
    plt.ylabel('Weight (lbs)', fontsize=12)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    
    # saving the figure
    plt.savefig('visualizations/weight_by_position_boxplot.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: visualizations/weight_by_position_boxplot.png")
    plt.close()





def main():
    """
    Run all statistical analyses
    """
    import os
    os.makedirs('visualizations', exist_ok=True)

    # Analyze all datasets
    df_players, stats_players = analyze_active_players()
    df_teams, stats_teams, correlation = analyze_team_performance()


    # Create correlation heatmaps
    # Team performance correlation heatmap
    team_corr_cols = ['W', 'L', 'OFF_RATING', 'DEF_RATING', 'NET_RATING']
    create_correlation_heatmap(df_teams, team_corr_cols,
                              'Team Performance Metrics Correlation Matrix',
                              'team_correlation_heatmap.png')



    # Player physical stats correlation
    player_corr_cols = ['height_in', 'weight']
    df_players_clean = df_players[player_corr_cols].dropna()
    
    
    # Only create heatmap if there is data
    if len(df_players_clean) > 0:
        create_correlation_heatmap(df_players_clean, player_corr_cols, 'Player Physical Attributes Correlation', 'player_correlation_heatmap.png')


    # Create boxplots
    create_boxplots()

    print("Analysis complete.")


if __name__ == "__main__":
    main()
