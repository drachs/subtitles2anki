#!/opt/conda/bin/python3

# Reads a CSV file of the format:
#   surface,reading,romaji,pos,frequency
# Uses AI to output a CSV file of the format:
#   surface,reading,romaji,pos,short_translation,detailed_translation,used_in_sentence,frequency

import sys
import pandas as pd
import os
import genanki

model_id = 1429503998
my_model = genanki.Model(
  model_id,
  'Japanese Vocabulary Model',
  fields=[
    {'name': 'Surface'},
    {'name': 'Reading'},
    {'name': 'Romaji'},
    {'name': 'Sentence'},
    {'name': 'Audio'},
    {'name': 'ShortTranslation'},
    {'name': 'DetailedTranslation'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '''
        <div>{{Surface}}</div>
        <div>{{Reading}} / {{Romaji}}</div>
        <div>{{Sentence}}</div>
        <div>{{Audio}}</div>
      ''',
      'afmt': '''
        {{FrontSide}}
        <hr id="answer">
        <div>{{ShortTranslation}}</div>
        <div>{{DetailedTranslation}}</div>
      ''',
    },
  ],
)

def load_manifest(show):
    with open(f"../subtitles/{show}/manifest.txt", "r") as f:
        return f.read().splitlines()

show = sys.argv[1]
files = load_manifest(show)

for file in files:
    load_filename = f"../enriched/{show}/{file}.csv"
    save_filename = f"{show}/{file}.apkg"
    deck_id = (hash(save_filename)%100000000)+(1 << 30)+10000
    # if save_filename already exists, skip
    if os.path.exists(save_filename):
        print(f"Skipping {save_filename} as it already exists")
        continue

    print(f"Generating Deck from {load_filename} and saving to {save_filename}")
    
    df = pd.read_csv(load_filename)

    my_deck = genanki.Deck(deck_id, f"{show} - {file}")

    audio_files = []
    for index, row in df.iterrows():
        audio = f"[sound:{row['reading']}.mp3]"
        audio_filename = f"../audio/files/{row['reading']}.mp3"
        if audio_filename not in audio_files:
            if not os.path.exists(audio_filename):
                print(f"Could not find {audio_filename}")
            print(f"Adding {audio} for {audio_filename}")
            audio_files.append(audio_filename)

        my_note = genanki.Note(
          model=my_model,
          fields=[row['surface'], row['reading'], row['romaji'], row['used_in_sentence'], audio, row['short_translation'], row['detailed_translation']]
        )
        my_deck.add_note(my_note)

    package = genanki.Package(my_deck)
    package.media_files = audio_files
    package.write_to_file(save_filename)
    break
