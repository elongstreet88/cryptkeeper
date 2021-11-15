# Overview
Simple transaction tracker website.
No fluff, just simple transaction info.

# Requirements
- Python 3.9+

# Getting Started
- For first time run: `./initialize.sh` (only needed to run once)
- Django web server can be started any time after that via vscode debugger `launch.json` included or manually via `python ./main/manage.py runserver`

# Changelog

## 0.13.0 (Nov 14, 2021)

FEATURES:
* Refactor coinbase importer to support convert
* Added type `send` and `airdrop`
* Added export all for transcations


ENHANCEMENTS:

BUG FIXES:

---

## 0.12.0 (Oct 27, 2021)

FEATURES:
* Blockfi importer partially working
* Added `import_hash` field to `transaction` to allow users to edit fields and re-importing doesn't override them
* Added `delete all transcations` capability

ENHANCEMENTS:

BUG FIXES:

---

## 0.11.0 (Oct 21, 2021)

FEATURES:
* API uploader front end converted to ajax
* File importer returns row counts
* Fixed icons
* Mockup of charting on home page

ENHANCEMENTS:

BUG FIXES:

---

## 0.10.0 (Oct 20, 2021)

FEATURES:
* Coinbase importer mockup working
* `Fee` field added
* Multi-select delete working on `transactions`

ENHANCEMENTS:

BUG FIXES:

---

## 0.9.0 (Oct 19, 2021)

FEATURES:
* Multi select exclusion of last row to avoid buttons causing selection
* Working upload API

ENHANCEMENTS:

BUG FIXES:
* Removed .ds_store files

---

## 0.8.0 (Oct 19, 2021)

FEATURES:
* Multi select on datatables working
* Fixed some styling for datatables

ENHANCEMENTS:

BUG FIXES:

---

## 0.7.0 (Oct 18, 2021)

FEATURES:
* `PUT`, `UPDATE`, `DELETE` all implemented
* UI CRUD for transactions working
* TODO: Cleanup JS and write tests

ENHANCEMENTS:

BUG FIXES:

---

## 0.6.0 (Oct 16, 2021)

FEATURES:
* Working `put` example with toast
* TODO: lock down the rest of the api methods and cleanup UI

ENHANCEMENTS:

BUG FIXES:

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