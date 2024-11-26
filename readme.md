# README

flood_bot is a script used to identifying flood alerts and flood warnings within the UK. It uses OpenAI and the UK GOV environmental flood monitoring API to grab data regarding flood information in a particular county.

## requisites

Use pip to install requirements.txt

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