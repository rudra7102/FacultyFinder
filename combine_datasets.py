import pandas as pd

faculty_df = pd.read_csv(
    "data/processed/final_faculty_profiles.csv"
)

other_df = pd.read_csv(
    "data/processed/other_faculty.csv"
)

combined_df = pd.concat(
    [faculty_df, other_df],
    ignore_index=True
)

combined_df.drop_duplicates(
    subset=["name"],
    inplace=True
)

combined_df.to_csv(
    "data/processed/final_combined_faculty.csv",
    index=False
)

print("Combined dataset created")
print("Total records:", len(combined_df))