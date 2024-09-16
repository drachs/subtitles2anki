#!/opt/conda/bin/python3

# Reads a CSV file of the format:
#   surface,reading,romaji,pos,frequency
# Uses AI to output a CSV file of the format:
#   surface,reading,romaji,pos,short_translation,detailed_translation,used_in_sentence,frequency

import sys
import pandas as pd
import os
from openai import OpenAI

def load_manifest(show):
    with open(f"../subtitles/{show}/manifest.txt", "r") as f:
        return f.read().splitlines()

# Load openai key from environment

openai_key = os.getenv("OPENAI_KEY")
if not openai_key:
    print("Please set the OPENAI_KEY environment variable.")
    sys.exit(1)

client = OpenAI(api_key = openai_key)

show = sys.argv[1]
files = load_manifest(show)

max_files = 700
current_files = 0

for file in files:
    load_filename = f"../enriched/{show}/{file}.csv"
    
    # If load_filename does not exist, exit
    if not os.path.exists(load_filename):
        print(f"File {load_filename} does not exist")
        sys.exit(1)

    print(f"Generating audio data for {load_filename}")
    
    df = pd.read_csv(load_filename)

    # for each row in df generate an audio file for the reading
    for index, row in df.iterrows():
        reading = row['reading']

        save_filename = f"files/{reading}.mp3"
        if os.path.exists(save_filename):
            print(f"Skipping {save_filename} as it already exists")
            continue

        # generate audio file
        response = client.audio.speech.create(
            model="tts-1",
            voice="onyx",
            input=reading
        )

        response.stream_to_file(save_filename)
        print(f"Generated {save_filename}")

        current_files += 1
        if current_files >= max_files:
            print("Reached max files, only doing {max_files} files per run")
            sys.exit(0)
    


