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
        <div class="box">
          <div class="label">Surface</div>
          <div>{{Surface}}</div>
        </div>

        <div class="box">
          <div class="label">Reading / Romaji</div>
          <div>{{Reading}} / {{Romaji}}</div>
        </div>

        <div class="box">
          <div class="label">Sentence</div>
          <div>{{Sentence}}</div>
        </div>

        <div class="box">
          <div class="label">Audio</div>
          <div>{{Audio}}</div>
        </div>
        ''',
      'afmt': '''
        {{FrontSide}}
        <hr id="answer">

        <div class="box">
          <div class="label">Short Translation</div>
          <div class="short-answer">{{ShortTranslation}}</div>
        </div>

        <div class="box">
          <div class="label">Detailed Translation</div>
          <div class="detailed-answer">{{DetailedTranslation}}</div>
        </div>
        ''',
    },
  ],
  css='''
    .card {
      font-family: Arial, sans-serif;
      font-size: 30px;
      text-align: center;
      color: #333;
      background-color: #f0f8ff; /* Light blue background of the card */
      padding: 20px;
      border-radius: 15px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Soft shadow */
    }

    /* Setting the background outside the card */
    body {
      background-color: white;
    }

    .box {
      background-color: #e6f7ff; /* Light blue box color */
      padding: 15px;
      margin: 10px 0;
      border-radius: 10px;
      border: 1px solid #b3e0ff; /* Light blue border */
    }

    .label {
      font-weight: bold;
      color: #007acc; /* Darker blue color */
      margin-bottom: 5px;
    }

    .short-answer {
      font-size: 40px;
      font-weight: bold;
      color: #007acc; /* Darker blue */
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

