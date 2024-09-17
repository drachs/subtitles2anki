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
  'Sutanki Immersion',
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
        <div class="short-answer">{{ShortTranslation}}</div>
        <br><br>
        <div class="detailed-answer">{{DetailedTranslation}}</div>
      ''',
    },
  ],
  css='''
    .card {
      font-family: arial;
      font-size: 30px;
      text-align: center;
      color: black;
      }

    .short-answer {
      font-size: 40px;
      font-weight: bold;
    }

    .detailed-answer {
      color: blue;
    }
  ''',
)

def load_manifest(show):
    with open(f"../subtitles/{show}/manifest.txt", "r") as f:
        return f.read().splitlines()

show = sys.argv[1]
files = load_manifest(show)

for file in files:
    load_filename = f"../enriched/{show}/{file}.csv"
    save_filename = f"{show}/{file}.apkg"
    deck_id = 1241591403 # Random number, same for all decks so they'll merge

    # If load_filename does not exist, exit
    if not os.path.exists(load_filename):
        print(f"File {load_filename} does not exist")
        sys.exit(1)

    print(f"Generating Deck from {load_filename} and saving to {save_filename}")
    
    df = pd.read_csv(load_filename)

    my_deck = genanki.Deck(deck_id, f"Sutanki Immersion")

    audio_files = []
    for index, row in df.iterrows():
        audio = f"[sound:{row['reading']}-{row['pos']}.mp3]"
        audio_filename = f"../audio/files/{row['reading']}-{row['pos']}.mp3"
        if audio_filename not in audio_files:
            if not os.path.exists(audio_filename):
                print(f"Could not find {audio_filename}")
            audio_files.append(audio_filename)

        note_guid = genanki.guid_for(row['reading'], row['pos'])

        my_note = genanki.Note(
          model=my_model,
          fields=[row['surface'], row['reading'], row['romaji'], row['used_in_sentence'], audio, str(row['short_translation']), row['detailed_translation']],
          guid=note_guid
        )
        my_deck.add_note(my_note)

    package = genanki.Package(my_deck)
    package.media_files = audio_files
    package.write_to_file(save_filename)

