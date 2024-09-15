#!/opt/conda/bin/python3

# Tokenizes the subtitles and saves them in a csv file of the format sorted descending by frequency
# surface,reading,pos,frequency

import MeCab
import unidic_lite
import pandas as pd
import sys
import re
import os

def load_manifest(show):
    with open(f"../subtitles/{show}/manifest.txt", "r") as f:
        return f.read().splitlines()

def extract_text_from_srt(file_path):
    with open(file_path, 'r') as f:
        file_content = f.read()

        cleaned_text = re.sub(r'\d+\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\n', '', file_content)
    return cleaned_text

def tokenize_text(text):
    tagger = MeCab.Tagger("-d " + unidic_lite.DICDIR)
    # Parse the input text
    parsed = tagger.parse(text)

    parsed_rows = []
    # Process and extract information
    for line in parsed.splitlines():
        if line == 'EOS':
            break

        # Split the line into parts based on tabs
        parts = line.split('\t')
        
        # Ensure the line has enough fields to extract
        if len(parts) < 5:
            print("****SKIPPING LINE****: ", line)
            continue  # Skip lines that do not have the expected number of fields

        surface = parts[0]  # Surface form
        reading = parts[1]  # Reading
        pos = parts[4]  # Part-of-speech
        
        parsed_rows.append((surface, reading, pos))
        
    df = pd.DataFrame(parsed_rows, columns=['surface', 'reading', 'pos'])
    return df

def cleanup(df):
    df = df.groupby(["surface", "reading", "pos"]).size().reset_index(name="frequency")
    df = df.sort_values(by="frequency", ascending=False)
    
    return df

show = sys.argv[1]
files = load_manifest(show)
for file in files:
    load_filename = f"../subtitles/{show}/{file}"
    save_filename = f"{show}/{file}.csv"
    print(f"Tokenizing {load_filename} and saving to {save_filename}")
    text = extract_text_from_srt(load_filename)
    df = tokenize_text(text)
    df_frequency = cleanup(df)

    df_frequency.to_csv(save_filename, index=False)


