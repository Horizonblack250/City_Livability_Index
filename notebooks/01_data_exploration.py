import pandas as pd
import os

datasets = {
    "AQI": r"C:\Users\alokhande\Desktop\Project_Daedalus\Global_Air_Pollution_Dataset\global air pollution dataset.csv",
    "Cost_of_Living_v1": r"C:\Users\alokhande\Desktop\Project_Daedalus\Global_Cost_Of_Living\cost-of-living.csv",
    "Cost_of_Living_v2": r"C:\Users\alokhande\Desktop\Project_Daedalus\Global_Cost_Of_Living\cost-of-living_v2.csv",
    "Pop_Density_1": r"C:\Users\alokhande\Desktop\Project_Daedalus\population_Density_Data\CCCdata1.csv",
    "Pop_Density_2": r"C:\Users\alokhande\Desktop\Project_Daedalus\population_Density_Data\CCCdata2.csv",
    "Crime_Index": r"C:\Users\alokhande\Desktop\Project_Daedalus\World_Crime_Index_Safety_Index\crime-index-2023.csv",
}

for name, path in datasets.items():
    print(f"\n{'='*60}")
    print(f"  {name}")
    print(f"{'='*60}")
    try:
        df = pd.read_csv(path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding='latin-1')

    print(f"Shape        : {df.shape[0]} rows x {df.shape[1]} cols")
    print(f"\nColumns ({df.shape[1]}):")
    for col in df.columns:
        print(f"  - {col}  [{df[col].dtype}]  | nulls: {df[col].isnull().sum()}")
    print(f"\nFirst 3 rows:")
    print(df.head(3).to_string())
    print(f"\nBasic stats (numeric only):")
    print(df.describe().to_string())