# Overview
Simple transaction tracker website.
No fluff, just simple transaction info.

# Requirements
- Python 3.9+

# Getting Started
- For first time run: `./initialize.sh` (only needed to run once)
- Django web server can be started any time after that via vscode debugger `launch.json` included or manually via `python ./main/manage.py runserver`

# Changelog

## 0.7.0 (Oct 18, 2021)

FEATURES:
* `PUT`, `UPDATE`, `DELETE` all implemented
* UI CRUD for transactions working
* TODO: Cleanup JS and write tests

ENHANCEMENTS:

BUG FIXES:
* Admin registration fix

---

## 0.6.0 (Oct 16, 2021)

FEATURES:
* Working `put` example with toast
* TODO: lock down the rest of the api methods and cleanup UI

ENHANCEMENTS:

BUG FIXES:
* Admin registration fix

---

## 0.5.0 (Oct 14, 2021)

FEATURES:
* Datatables rest api with django wired up and working transactions page
* TODO: Cleanup buttons and ajax crud from js
* Added `from` an `to` for into model `transaction`

ENHANCEMENTS:

BUG FIXES:
* Admin registration fix

---

## 0.4.0 (Oct 12, 2021)

FEATURES:
* Django Rest Framework wired up. Will need cleaned up arrangement
* Basic user data filtered rest api added

ENHANCEMENTS:

BUG FIXES:

---

## 0.3.0 (Oct 12, 2021)

FEATURES:
* Working user data association
* Base template created.

ENHANCEMENTS:

BUG FIXES:

---

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