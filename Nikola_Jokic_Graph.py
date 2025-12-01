import pandas as pd
import matplotlib.pyplot as plt

def load_jokic():
    df = pd.read_csv("cleaned_csv/Nikola_Jokic_Info_CLEANED.csv")
    return df

def plot_jokic_stats_over_time(df):
    df["SEASON"] = df["SEASON_ID"].astype(str).str[-2:].astype(int) + 2000  # Convert to year format

    plt.figure()
    plt.plot(df["SEASON"], df["PTS"], marker="o")
    plt.title("Nikola Jokic Total Points by Season")
    plt.xlabel("Season")
    plt.ylabel("Points")
    plt.grid(True)
    plt.show()

    plt.figure()
    plt.plot(df["SEASON"], df["REB"], marker="o")
    plt.title("Nikola Jokic Total Rebounds by Season")
    plt.xlabel("Season")
    plt.ylabel("Rebounds")
    plt.grid(True)
    plt.show()

    plt.figure()
    plt.plot(df["SEASON"], df["AST"], marker="o")
    plt.title("Nikola Jokic Total Assists by Season")
    plt.xlabel("Season")
    plt.ylabel("Assists")
    plt.grid(True)
    plt.show()



if __name__ == "__main__":
    df = load_jokic()
    plot_jokic_stats_over_time(df)
    
