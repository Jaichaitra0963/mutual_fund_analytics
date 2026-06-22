import pandas as pd
import os

folder = "data/raw/"
files = [f for f in os.listdir(folder) if f.endswith(".csv")]

print(f"Total CSV files found: {len(files)}")

for file in files:
    df = pd.read_csv(folder + file)
    print(f"\n=== {file} ===")
    print("Shape:", df.shape)
    print("Columns:", list(df.columns))
    print("Missing values:", df.isnull().sum().sum())
    print(df.head(3))

print("\n--- Data Quality Summary ---")
print(f"Total files loaded: {len(files)}")
