# Overview
Simple transaction tracker website.
No fluff, just simple transaction info.

I really hate most of the crypto portfolio apps out there, both paid and free.
They don't handle transactions cleanly and who knows what they are doing behind the scenes.

The goal of this project is to provide an open source web based portfolio manager that anyone can use.

# Tech Stack
- Django
- Python
- Javascript
- HTML5
- JQuery
- Bootstrap
- SQLLite
- AdminLTE 3 (aka the best html5 theme out there)

# Features
- Self contained (no external dependencies besides coinbase api call for price lookups)
- No API keys required (for now)
- Transaction Importers for
  - Blockfi
  - Coinbase
  - Celcius (comming soon)
  - Binance.US (coming soon)
- Simple data tables with full export
- Auth on by default (google auth can be turned on, local django auth works fine too)
- Forever free, always open source

# How to support
- PR requests always welcome
- Dontate via BTC!
```
BTC Address: 3DDqESKCb6nXeNbEniqsmCSgzHd2Sk6nuU
```

# Requirements
- Python 3.9+

# Getting Started
- For first time run: `./initialize.sh` (only needed to run once)
- Django web server can be started any time after that via vscode debugger `launch.json` included or manually via `python ./main/manage.py runserver`

# Changelog
[Current](CHANGELOG.md)