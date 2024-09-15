# Anki Card Generator for Arbitrary Subtitles

I am writing this as I try to get into immersion while studing Japanese.  I am very new to Japanese, so I'm sure this could be 
improved by help from people with more experience.

The goal here is to facilitate my ability to watch a show in Japanese by generating an Anki deck for the show, and to generate
incremental Anki decks for following shows.  The first show I'm going to use to experiment with is the origional Naruto.

## Step 1 - Subtitles are obtained and stationed in the subtitles folder
Subtitles are stationed in data/subtitles/<show>

These subtitles will not be included in the repo because they could potentially be copyrighted.  There will be a manifest file however.

## Step 2 - Subtitles are tokenized into a non-copyrightable raw format
These tokenized files will be stored in data/tokenized/<show>/<episode_name>.srt.csv

These token files will be as raw as possible while being clearly not subject to copyright.  The format I have chosen is a csv 
database in the following form sorted by frequency descending: 

surface,reading,pos,frequency

## Step 3 - Filtering
These files will contain all kinds of stuff that should probably be filtered out, but the filtering might be the subject of many interesting
pull requests so I'd like to commit some raw ugly data here so we can all inovvate on good filter.  Examples of uglyness in these files
include english words, symbols, etc.

