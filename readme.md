# README

flood_bot is a script used for identifying flood alerts and flood warnings within the UK. It uses OpenAI and the UK GOV environmental flood monitoring API to gab data regarding flood information in a particular county

Spoticloud-dl is a script to download playlists from either Spotify or Soundcloud with a max bandwidth of either 320kbps or 128kbps respectively. The script also appends metadata to the mp3s, including album art, artist and album name if applicable. 

## requisites

Use the pip to install requirements.txt

```bash
pip install requirements.txt
```

Set up your Azure key and endpoint

```bash
set AZURE_KEY=your_key
```

```bash
set AZURE_ENDPOINT=your_endpoint
```


## Usage

- set up AZURE_KEY and AZURE_ENDPOINT as instructed above

- Run bot_final.py and ask it a question like "How many flood warnings are there in Wiltshire at the moment?"