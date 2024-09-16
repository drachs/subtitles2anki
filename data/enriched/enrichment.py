#!/opt/conda/bin/python3

# Reads a CSV file of the format:
#   surface,reading,romaji,pos,frequency
# Uses AI to output a CSV file of the format:
#   surface,reading,romaji,pos,short_translation,detailed_translation,used_in_sentence,frequency

import sys
import pandas as pd
import os
from openai import OpenAI

pos_prompt = """

Please translate the provided japanese word into english.
You will be provided with the part of speech.

Your output should be json and look like this:

{
  "short_translation": "string"
  "english_pos": "string"
  "detailed_translation": "string"
  "used_in_sentence": "string"
}

short_translation: Contains a short one or two word english translation.
english_pos: Contains the part of speech in english.
detailed_translation: Contains a more detailed explanation of the translation in english with possible additional meanings.
used_in_sentence: Contains a japanese languge sentence where the word is used.

Here is the part of speech: """

word_prompt = "\nHere is the word:"

def load_manifest(show):
    with open(f"../subtitles/{show}/manifest.txt", "r") as f:
        return f.read().splitlines()

# translate
def translate(surface, pos):
    prompt = pos_prompt + pos + word_prompt + surface
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",  # Use the appropriate model
        messages=[{"role":"system", "content": prompt}],
        response_format=Translation
    )

    message = completion.choices[0].message
    if message.parsed is None:
        return None

    return pd.Series([message.parsed.short_translation, message.parsed.detailed_translation, message.parsed.used_in_sentence])

from pydantic import BaseModel
class Translation(BaseModel):
    short_translation: str
    english_pos: str
    detailed_translation: str
    used_in_sentence: str

# Load openai key from environment

openai_key = os.getenv("OPENAI_KEY")
if not openai_key:
    print("Please set the OPENAI_KEY environment variable.")
    sys.exit(1)

client = OpenAI(api_key = openai_key)

show = sys.argv[1]
files = load_manifest(show)

max_files = 1
current_files = 0

for file in files:
    load_filename = f"../filtered/{show}/{file}.csv"
    save_filename = f"{show}/{file}.csv"
    # if save_filename already exists, skip
    if os.path.exists(save_filename):
        print(f"Skipping {save_filename} as it already exists")
        continue

    print(f"Enriching {load_filename} and saving to {save_filename}")
    
    df = pd.read_csv(load_filename)
    df[['short_translation', 'detailed_translation', 'used_in_sentence']] = df.apply(
    lambda row: translate(row['surface'], row['pos']), axis=1
    )

    df.to_csv(save_filename, index=False)

    current_files += 1
    if current_files >= max_files:
        printf("Reached max files, only doing {max_files} files per run")
        sys.exit(0)
    


