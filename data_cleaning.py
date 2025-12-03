"""
NBA Data Cleaning Module

This module handles comprehensive data cleaning for all NBA datasets.
Each cleaning function documents the issues found, decisions made, and impact.

Cleaning Strategy:
- Missing values: Strategic handling based on column importance
- Duplicates: Removed to ensure data integrity
- Outliers: Careful validation before removal (NBA has legitimate extremes)
- Formatting: Standardized text and data types for analysis
"""

import json
import pandas as pd
import numpy as np
import os


def clean_data():
    """Running all cleaning functions and create output directories"""
    
    # creating /uncleaned_csv directory if it doesn't exist
    os.makedirs('cleaned_csv', exist_ok=True)
    
    
    # cleaning all csv files found in /uncleaned_csv folder
    clean_get_all_teams()
    clean_get_all_players_of_all_time()
    clean_single_player_by_id()
    clean_player_info_by_full_name()
    clean_ACTIVE_PLAYERS()
    clean_advanced_team_stats()
    clean_league_standings()

    print("\nData cleaning complete")
    
    

"""
1. Cleaning the NBA Teams CSV
   Output: "nba_teams_CLEANED.csv"

   Issues Addressed:
   - Missing values in team information
   - Duplicate team entries
   - Inconsistent text formatting

   Cleaning Decisions:
   - Missing values: Fill with 'Unknown' (team data is typically complete)
   - Duplicates: Remove (teams should be unique)
   - Text formatting: Standardize to title case for consistency
"""
def clean_get_all_teams():
    print("\n Cleaning NBA Teams dataset...")
    df = pd.read_csv("uncleaned_csv/nba_teams.csv")


    # 1. Handle missing values
    df.fillna('Unknown', inplace=True)

    # 2. Remove duplicates
    df.drop_duplicates(inplace=True)

    # 3. Formatting
    df['full_name'] = df['full_name'].str.strip().str.title()

    # Save the cleaned data
    df.to_csv("cleaned_csv/nba_teams_CLEANED.csv", index=False)


    print("\nCleaned data saved to cleaned_csv/nba_teams_CLEANED.csv")




"""
2. Cleaning the All Players of All Time CSV
   Output: "all_players_CLEANED.csv"

   Issues Addressed:
   - Missing values in player names or IDs
   - Duplicate player entries
   - Inconsistent text formatting in names

   Cleaning Decisions:
   - Missing values: Fill with 'Unknown' to maintain record existence
   - Duplicates: Remove to ensure unique player records
   - Text formatting: Standardize first and last names to title case
"""
def clean_get_all_players_of_all_time():
    # Load the data
    df = pd.read_csv("uncleaned_csv/all_players.csv")
    
    print(f"Original shape: {df.shape}")
    print(f"Missing values:\n{df.isnull().sum()}")
    
    # Example cleaning steps
    # 1. Handle missing values
    df.fillna('Unknown', inplace=True)
    
    # 2. Remove duplicates
    df.drop_duplicates(inplace=True)
    
    # 3. Formatting
    df['first_name'] = df['first_name'].str.strip().str.title()
    df['last_name'] = df['last_name'].str.strip().str.title()
    
    print(f"\nCleaned shape: {df.shape}")
    print(f"Remaining missing values:\n{df.isnull().sum()}")
    
    # Save the cleaned data
    df.to_csv("cleaned_csv/all_players_CLEANED.csv", index=False)
    print("\nCleaned data saved to cleaned_csv/all_players_CLEANED.csv")
    




"""
3. Cleaning Single Player by ID CSV
   Output: "Nikola_Jokic_Info_CLEANED.csv"

   Issues Addressed:
   - Unnecessary index columns from raw export
   - Missing values in statistical columns (numeric and categorical)
   - Duplicate entries
   - Inconsistent formatting in team abbreviations
   - Incorrect data types (e.g., Age as string)

   Cleaning Decisions:
   - Unnamed columns: Dropped artifacts
   - Missing numeric: Filled with 0 assuming no stats recorded
   - Missing categorical: Filled with 'Unknown'
   - Duplicates: Removed
   - Formatting: Team abbreviations standardized to uppercase
   - Data Types: Converted Age to float for numerical analysis
"""
def clean_single_player_by_id():
    # Load the data
    df = pd.read_csv("uncleaned_csv/Nikola_Jokic_Info.csv")
    
    print(f"Original shape: {df.shape}")
    print(f"Missing values:\n{df.isnull().sum()}")
    
    # 1. Drop the unnamed index column
    df = df.drop(df.columns[0], axis=1)
    
    # 2. Handle missing values in numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].fillna(0)
    
    # 3. Handle missing values in categorical columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        df[col].fillna('Unknown', inplace=True)
    
    # 4. Remove duplicates
    df.drop_duplicates(inplace=True)
    
    # 5. Format team abbreviation
    if 'TEAM_ABBREVIATION' in df.columns:
        df['TEAM_ABBREVIATION'] = df['TEAM_ABBREVIATION'].str.strip().str.upper()
    
    # 6. Ensure proper data types
    if 'PLAYER_AGE' in df.columns:
        df['PLAYER_AGE'] = df['PLAYER_AGE'].astype(float)
    
    print(f"\nCleaned shape: {df.shape}")
    print(f"Remaining missing values:\n{df.isnull().sum()}")
    
    # Save the cleaned data
    df.to_csv("cleaned_csv/Nikola_Jokic_Info_CLEANED.csv", index=False)
    print("\nCleaned data saved to cleaned_csv/Nikola_Jokic_Info_CLEANED.csv")
 
 
    
    
"""
4. Cleaning Player Info by Full Name CSV
   Output: "AlexAbrines_CLEANED.csv"

   Issues Addressed:
   - Missing values in player details
   - Duplicate records
   - Inconsistent capitalization in names

   Cleaning Decisions:
   - Missing values: Fill with 'Unknown'
   - Duplicates: Remove to ensure unique records
   - Text formatting: Standardize names to title case for consistency
"""
def clean_player_info_by_full_name():
    # Load the data
    df = pd.read_csv("uncleaned_csv/AlexAbrines.csv")
    
    print(f"Original shape: {df.shape}")
    print(f"Missing values:\n{df.isnull().sum()}")
    
    # Example cleaning steps
    # 1. Handle missing values
    df.fillna('Unknown', inplace=True)
    
    # 2. Remove duplicates
    df.drop_duplicates(inplace=True)
    
    # 3. Formatting
    df['first_name'] = df['first_name'].str.strip().str.title()
    df['last_name'] = df['last_name'].str.strip().str.title()
    
    print(f"\nCleaned shape: {df.shape}")
    print(f"Remaining missing values:\n{df.isnull().sum()}")
    
    # Save the cleaned data
    df.to_csv("cleaned_csv/AlexAbrines_CLEANED.csv", index=False)
    print("\nCleaned data saved to cleaned_csv/AlexAbrines_CLEANED.csv")






"""
5. Cleaning Active Players CSV
   Output: "ACTIVE_PLAYERS_CLEANED.csv"

   Issues Addressed:
   - Missing values in name fields (critical - player identification)
   - Missing values in numeric fields (height, weight, etc.)
   - Duplicate player entries
   - Outliers in physical measurements
   - Inconsistent text formatting

   Cleaning Decisions:
   - Missing names: Dropped (cannot identify player without name)
   - Missing numeric values: Filled with median (preserves distribution)
   - Outliers: REMOVED using IQR method
     WARNING: This may remove legitimate NBA players with extreme measurements
     (e.g., very tall centers like Boban Marjanovic, or shorter guards)
     Consider reviewing this decision for production analysis
   - Text formatting: Standardized to title case for consistency

   Impact: Outlier removal may reduce dataset by 5-15% depending on distributions
"""
def clean_ACTIVE_PLAYERS():
    print("\nCleaning Active Players dataset...")
    df = pd.read_csv("uncleaned_csv/ACTIVE_PLAYERS.csv")


    # 1. Handle missing values (strategic approach)
    # Drop rows where critical columns are missing
    df.dropna(subset=['first_name', 'last_name'], inplace=True)

    # Fill numeric columns with median (more robust than mean for skewed data)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

    # Fill categorical columns with 'Unknown'
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        df[col].fillna('Unknown', inplace=True)

    # 2. Remove duplicates
    df.drop_duplicates(inplace=True)

    # 3. Handle outliers - NOTE: This is aggressive and may remove valid players
    original_before_outliers = len(df)
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]

    print(f"Outlier removal: {original_before_outliers - len(df)} rows removed ({((original_before_outliers - len(df))/original_before_outliers*100):.1f}%)")

    # 4. Formatting - standardize text columns
    for col in categorical_cols:
        df[col] = df[col].str.strip().str.title()

    # Save the cleaned data
    df.to_csv("cleaned_csv/ACTIVE_PLAYERS_CLEANED.csv", index=False)


    print("Saved: cleaned_csv/ACTIVE_PLAYERS_CLEANED.csv")
    




"""
6. Cleaning the Advanced Team Stats CSV
   Output: "advanced_team_stats_CLEANED.csv"

   Issues Addressed:
   - Irrelevant columns for analysis
   - Inconsistent text formatting and data types
   - Missing values in critical metrics
   - Logical inconsistencies (e.g., Wins + Losses != Games Played)

   Cleaning Decisions:
   - Column Selection: Kept only relevant metrics (W, L, Ratings)
   - Formatting: Stripped whitespace, coerced numeric types
   - Missing Values: Dropped rows with missing critical data
   - Logic Checks: Verified GP > 0 and W + L consistency
"""
def clean_advanced_team_stats():
    print("\nCleaning: Advanced Team Stats...")
    input_path = 'uncleaned_csv/advanced_team_stats.csv'
    output_path = 'cleaned_csv/advanced_team_stats_CLEANED.csv'

    try:
        # Load the data
        df = pd.read_csv(input_path)

        # 1. Select Columns
        columns_to_keep = [
            'TEAM_NAME', 'GP', 'W', 'L', 
            'OFF_RATING', 'DEF_RATING', 'NET_RATING', 
            'W_RANK', 'L_RANK'
        ]
        # Only keep columns that actually exist in the file
        existing_cols = [col for col in columns_to_keep if col in df.columns]
        df_cleaned = df[existing_cols].copy()

        # 2. Formatting: Standardize Text & Types
        if 'TEAM_NAME' in df_cleaned.columns:
            # Remove leading/trailing whitespace
            df_cleaned['TEAM_NAME'] = df_cleaned['TEAM_NAME'].astype(str).str.strip()

        # Ensure numeric columns are actually numeric (coerce errors to NaN)
        numeric_cols = ['GP', 'W', 'L', 'OFF_RATING', 'DEF_RATING', 'NET_RATING']
        for col in numeric_cols:
            if col in df_cleaned.columns:
                df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce')

        # 3. Handle Missing Values
        initial_count = len(df_cleaned)
        df_cleaned.dropna(inplace=True) # Drop rows with ANY missing values in selected columns
        if len(df_cleaned) < initial_count:
            print(f"Dropped {initial_count - len(df_cleaned)} rows containing missing values.")

        # 4. Outliers & Logic Checks (Sanity Checks)
        # Rule: Games Played (GP) must be positive
        if 'GP' in df_cleaned.columns:
            df_cleaned = df_cleaned[df_cleaned['GP'] > 0]

        # Rule: Wins + Losses should equal Games Played
        # (This catches data entry errors)
        if {'W', 'L', 'GP'}.issubset(df_cleaned.columns):
            valid_games_mask = (df_cleaned['W'] + df_cleaned['L'] == df_cleaned['GP'])
            invalid_count = (~valid_games_mask).sum()
            
            if invalid_count > 0:
                print(f"Warning: {invalid_count} rows have W + L != GP. (Keeping them, but check source data).")
                # Uncomment the next line to strictly remove these rows:
                # df_cleaned = df_cleaned[valid_games_mask]

        # 5. Save to File
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        df_cleaned.to_csv(output_path, index=False)
        print(f"Saved cleaned data to {output_path}")

    except FileNotFoundError:
        print(f"File not found. Please ensure '{input_path}' exists.")
    except Exception as e:
        print(f"An error occurred during cleaning: {e}")
    print("\nCleaning: Advanced Team Stats...")
    
    try:
        df = pd.read_csv('uncleaned_csv/advanced_team_stats.csv')

        # Columns we want to keep
        columns_to_keep = [
            'TEAM_NAME', 
            'GP', 
            'W', 
            'L', 
            'OFF_RATING', 
            'DEF_RATING', 
            'NET_RATING', 
            'W_RANK', 
            'L_RANK'
        ]

        # Filter for existing columns only (avoids errors if API changes)
        existing_cols = [col for col in columns_to_keep if col in df.columns]
        df_cleaned = df[existing_cols]

        # Save to CLEANED folder
        output_path = 'cleaned_csv/advanced_team_stats_CLEANED.csv'
        df_cleaned.to_csv(output_path, index=False)
        print(f"Saved to {output_path}")

    except FileNotFoundError:
        print("File not found. Please ensure 'uncleaned_csv/advanced_team_stats.csv' exists.")
        
        
        

"""
7. Cleaning League Standings
   Output: "league_standings_CLEANED.csv"

   Issues Addressed:
   - Missing values in clinch indicators (often empty if not clinched)
   - Missing numeric values (e.g., Games Back)
   - Inconsistent text formatting in city/team names
   - Logical outliers in percentages and points per game

   Cleaning Decisions:
   - Clinch columns: Filled NaNs with 'No' (logical assumption)
   - Numeric NaNs: Filled with 0
   - Text formatting: Standardized to title case
   - Outliers: Filtered WinPCT (0-1) and PointsPG (60-160) to remove bad data
"""
def clean_league_standings():
    print("\nCleaning: League Standings...")
    try:
        df = pd.read_csv("uncleaned_csv/league_standings.csv")
        
        print(f"Original shape: {df.shape}")
        
        # 1. Handle Missing Values
        # Specific handling for clinch columns which are often empty/NaN
        clinch_cols = ['ClinchIndicator', 'ClinchedConferenceTitle', 'ClinchedDivisionTitle', 'ClinchedPlayoffBirth']
        for col in clinch_cols:
            if col in df.columns:
                df[col] = df[col].fillna('No') # Empty usually means they haven't clinched
        
        # Fill remaining numeric NaNs with 0 (e.g., GamesBack)
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(0)
        
        # Fill remaining text NaNs
        df.fillna('Unknown', inplace=True)

        # 2. Formatting
        if 'TeamCity' in df.columns:
            df['TeamCity'] = df['TeamCity'].str.strip().str.title()
        if 'TeamName' in df.columns:
            df['TeamName'] = df['TeamName'].str.strip().str.title()
            
        # 3. Handle Outliers
        # Logical check: WinPCT must be between 0 and 1
        if 'WinPCT' in df.columns:
            # Filter out impossible percentages
            df = df[(df['WinPCT'] >= 0.0) & (df['WinPCT'] <= 1.0)]
            
        # Logical check: PointsPG should be reasonable (e.g., 60 < PPG < 160)
        # This removes bad data rows without removing valid high/low performing teams
        if 'PointsPG' in df.columns:
            df = df[(df['PointsPG'] > 60) & (df['PointsPG'] < 160)]

        # Save
        output_path = "cleaned_csv/league_standings_CLEANED.csv"
        df.to_csv(output_path, index=False)
        print(f"Cleaned shape: {df.shape}")
        print(f"Saved to {output_path}")

    except FileNotFoundError:
        print("File not found. Please ensure 'uncleaned_csv/league_standings.csv' exists.")
    


# Call the function
clean_data()