# Anki Card Generator for Arbitrary Subtitles

I am writing this as I try to get into immersion while studing Japanese.  I am very new to Japanese, so I'm sure this could be 
improved by help from people with more experience.

The goal here is to facilitate my ability to watch a show in Japanese by generating an Anki deck for the show, and to generate
incremental Anki decks for following shows.  The first show I'm going to use to experiment with is the origional Naruto.

## Existing Decks
### Naruto
| Episode | Words | Deck Link
|---------|-------|----------
| 1 | 695
| 2 | 370
| 3 | 287
| 4 | 271
| 5 | 183
| 6 | 289
| 7 | 201
| 8 | 124
| 9 | 84
| 10 | 254
| 11 | 171
| 12 | 101
| 13 | 90
| 14 | 141
| 15 | 96

## Deck Generation

### Step 1 - Subtitles are obtained and stationed in the subtitles folder
Subtitles are stationed in data/subtitles/{show}

These subtitles will not be included in the repo because they could potentially be copyrighted.  There will be a manifest file however.

### Step 2 - Subtitles are tokenized into a non-copyrightable raw format
These tokenized files will be stored in data/tokenized/{show}/{episode_name}.srt.csv

These token files will be as raw as possible while being clearly not subject to copyright.  The format I have chosen is a csv 
database in the following form sorted by frequency descending: 

surface,reading,romaji,pos,frequency

surface: How the word appeared in the subtitles
reading: hiragana reading of the word
romaji: The surface represented in romaji
pos: Japanese part of speech
frequency: How often the word appeared in the show

These files will contain all kinds of stuff that should probably be filtered out, but the filtering might be the subject of many interesting
pull requests so I'd like to commit the raw ugly data here so we can all inovate on good filter.  Examples of uglyness in these files
include english words, symbols, punctuation, etc.

### Step 3 - Filtering
Filtered files will be stored in data/filtered/{show}/{episode_name}.srt.csv

Anything wierd like english words, symbols, punctuation, etc will be removed.
Each file after the first will only have words that haven't appeared in previous files for the show.

### Step 4 - AI Enrichment
Here we're using a GPT-4o to further enrich the data.  We're going to ask it to remove anything it thinks is wierd, as well as provide us 
with a single word translation, a longer more detailed translation, use the word in a sentence, and translate the part of speech.

surface,reading,romaji,pos,frequency,short_translation,detailed_translation,used_in_sentence

### Step 5 - Audio Generation
