import pandas as pd
import sys
import os

# python automation.py jury1.csv jury2.csv jury3.csv


def main():

    file_paths = sys.argv[1:]
    dataframes = []

    for file in file_paths:
        if not os.path.exists(file):
            print(f"Файлът {file} не съществува.")
            return

        df = pd.read_csv(file)
        df = df.set_index("ID")
        dataframes.append(df)

    categories = [
        col for col in dataframes[0].columns
        if col not in ["Име", "Резултат"]
    ]

    merged_df = pd.DataFrame()
    merged_df["Име"] = dataframes[0]["Име"]

    for category in categories:
        merged_df[category] = sum(df[category] for df in dataframes) / len(dataframes)

    merged_df["Резултат"] = merged_df[categories].sum(axis=1)
    merged_df = merged_df.sort_values(by="Резултат", ascending=False)

    merged_df.insert(0, "Място", range(1, len(merged_df) + 1))
    merged = merged_df.reset_index()

    merged.to_excel("final_ranking.xlsx", index=False)
    print("✅️Създаден е final_ranking.xlsx")


if __name__ == "__main__":
    main()
