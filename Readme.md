# Sutanki Immersion - Anki Card Generator for Arbitrary Subtitles

I am writing this as I try to get into immersion while studing Japanese.  I am very new to Japanese, so I'm sure this could be 
improved by help from people with more experience.

The goal here is to facilitate my ability to watch a show in Japanese by generating an Anki deck for the show, and to generate
incremental Anki decks for following shows.

The idea is that I can pull all these decks up online and if you want to watch Naruto you can grab Naruto episode one and work that deck until you're ready to watch the show.  Then watch the show, and merge in episode 2.  Each deck will be fully modular and the GUIDS will be stable so you can merge a new show into your deck at any time, and not have to relearn cards you already know. 

I hope it will be a fun way for people to do immersion.

If you want me to cook a deck for you please feel free to file an issue with instructions on how to find subtitles for the show and I'll include it here.

(Warning, pretty hot of the presses - probably buggy, maybe garbage - please provide feedback)

## Existing Decks

[Deck Folders](https://github.com/drachs/subtitles2anki/tree/main/data/decks)

## Todo
* ~~Eliminate Particles - I don't think flashcards are a good way to learn particles and it's very unsatisfying~~
* ~~Add the sentence to the voice~~
* ~~Global caches for AI generation based on reading-pos indexing~~
* ~~remove duplicates of reading-pos~~
* ~~updating a deck adds all the modified cards as new cards~~
* ~~Better control generation of audio as word[pause]sentence[pause]word~~
* Get the AI to produce simpler example sentences
* Do a nice layout design for the deck
* Add the english part of speech to the deck
* Build decks for the first 10 episodes of Naruto
* Build decks for the first episode of the 10 most popular anime series
* Upload an example deck for each series to ankiweb
* Establish a website
* Sometimes the sentence produced doesn't match the reading - for example the word Mono 者 has two readings


## Deck Generation

### Step 1 - Subtitles are obtained and stationed in the subtitles folder
Subtitles are stationed in data/subtitles/{show}

These subtitles will not be included in the repo because they could potentially be copyrighted.  There will be a manifest file however that
lists the subtitles in order and all future operations use that manifest as a guide.

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

Translations are cached according to reading-pos in the translation_cache folder

surface,reading,romaji,pos,frequency,short_translation,detailed_translation,used_in_sentence

### Step 5 - Audio Generation
Use openai to generate an audio file for each reading.

Audio files are cached according to reading.pos in the audio folder.

### Step 6 - Anki card generation
Data from the above steps is combined into Anki cards.