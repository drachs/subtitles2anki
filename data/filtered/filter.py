#!/opt/conda/bin/python3

import sys
import pandas as pd

def load_manifest(show):
    with open(f"../subtitles/{show}/manifest.txt", "r") as f:
        return f.read().splitlines()

def filters(df):
    # Filter out anything that's just non-letters and whitespace
    df = df[~df['surface'].str.contains(r'^[\W\s]+$', na=False)]
    
    # Filter out anything that's only ascii (Probably english words)
    df = df[~df['surface'].str.contains(r'^[\x00-\x7F]+$', na=False)]

    # Filter out any row where a column is NaN
    df = df.dropna()
    return df


df_previous = pd.DataFrame(columns=['surface', 'reading', 'romaji', 'pos', 'frequency'])
def incremental(df):
    global df_previous

    # Merge DataFrames on 'reading' and 'pos' to identify matching rows
    merged_df = df.merge(df_previous[['reading', 'pos']], on=['reading', 'pos'], how='left', indicator=True)

    # Filter out rows from df1 where there was a match in df2
    df_filtered = merged_df[merged_df['_merge'] == 'left_only'].drop(columns=['_merge'])

    df_previous = pd.concat([df_previous, df_filtered], ignore_index=True)
    return df_filtered


show = sys.argv[1]
files = load_manifest(show)
for file in files:
    load_filename = f"../tokenized/{show}/{file}.csv"
    save_filename = f"{show}/{file}.csv"
    print(f"Filtering {load_filename} and saving to {save_filename}")
    
    df = pd.read_csv(load_filename)
    df = filters(df)
    df = incremental(df)
    
    df.to_csv(save_filename, index=False)
