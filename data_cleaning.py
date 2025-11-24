import json
import pandas as pd
import numpy as np

def clean_data():
    clean_get_all_teams()
    clean_get_all_players_of_all_time()
    clean_single_player_by_id()
    clean_player_info_by_full_name()
    clean_ACTIVE_PLAYERS()
    

def clean_get_all_teams():
    # Load the data
    df = pd.read_csv("uncleaned_csv/nba_teams.csv")
    
    print(f"Original shape: {df.shape}")
    print(f"Missing values:\n{df.isnull().sum()}")
    
    # Example cleaning steps
    # 1. Handle missing values
    df.fillna('Unknown', inplace=True)
    
    # 2. Remove duplicates
    df.drop_duplicates(inplace=True)
    
    # 3. Formatting
    df['full_name'] = df['full_name'].str.strip().str.title()
    
    print(f"\nCleaned shape: {df.shape}")
    print(f"Remaining missing values:\n{df.isnull().sum()}")
    
    # Save the cleaned data
    df.to_csv("cleaned_csv/nba_teams_CLEANED.csv", index=False)
    print("\nCleaned data saved to cleaned_csv/nba_teams_CLEANED.csv")


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

def clean_ACTIVE_PLAYERS():
    # Load the data
    df = pd.read_csv("uncleaned_csv/ACTIVE_PLAYERS.csv")
    
    print(f"Original shape: {df.shape}")
    print(f"Missing values:\n{df.isnull().sum()}")
    
    # 1. Handle missing values (more strategic than just ffill)
    # Drop rows where critical columns are missing
    df.dropna(subset=['first_name', 'last_name'], inplace=True)
    
    # Fill numeric columns with mean/median
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    
    # Fill categorical columns with mode or 'Unknown'
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        df[col].fillna('Unknown', inplace=True)
    
    # 2. Remove duplicates
    df.drop_duplicates(inplace=True)
    
    # 3. Handle outliers (example for numeric columns)
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
    
    # 4. Formatting
    # Standardize text columns
    for col in categorical_cols:
        df[col] = df[col].str.strip().str.title()
    
    # Convert data types if needed
    # df['some_date_column'] = pd.to_datetime(df['some_date_column'])
    
    print(f"\nCleaned shape: {df.shape}")
    print(f"Remaining missing values:\n{df.isnull().sum()}")
    
    # Save the cleaned data
    df.to_csv("cleaned_csv/ACTIVE_PLAYERS_CLEANED.csv", index=False)
    print("\nCleaned data saved to cleaned_csv/ACTIVE_PLAYERS_CLEANED.csv")
    



# Call the function
clean_data()