# Overview
Simple transaction tracker website.
No fluff, just simple transaction info.

# Requirements
- Python 3.9+

# Getting Started
- For first time run: `./initialize.sh` (only needed to run once)
- Django web server can be started any time after that via vscode debugger `launch.json` included or manually via `python ./main/manage.py runserver`

# Changelog

## 0.2.0 (Oct 7, 2021)

FEATURES:
* `Adminlte3` theme loaded!
* Structure adjusted a bit to be best practice

ENHANCEMENTS:

BUG FIXES:
* `.gitignore` updates

---

## 0.1.1 (Oct 7, 2021)

FEATURES:

ENHANCEMENTS:
* Added `initialize.sh` to generate the secret key
* Added to getting started

BUG FIXES:
* removed secret key from `main/settings.py` and replaced with `secret_key.txt` include (which is in .gitingore)
---

## 0.1.0 (Oct 7, 2021)

FEATURES:
* README.md setup
* Initial cut
* Google SSO working
* Basic transaction model setup

ENHANCEMENTS:

BUG FIXES: