# Changelog

## 0.21.0 (Dec 28, 2021)

FEATURES:
* Added asset summary API call (ex: `http://localhost:8000/api/asset-info/BTC/`)
* Added `needs_reviewed` to `transactions` to enable easier review statusing
* 

ENHANCEMENTS:

BUG FIXES:

---

## 0.20.0 (Nov 29, 2021)

FEATURES:
* Added ability to modify cryptkeeper.csv export and merge/match it back on import. This allows modifying locally for bulk operations.
* `import_hash` exported from datatable now to support this

ENHANCEMENTS:

BUG FIXES:

KNOWN ISSUES:
* Saving csv in excel wipes seconds from timestamp which causes `updates` to occur and loss of precision. Not a cryptkeeper problem but will probably cause some headaches.

---

## 0.19.0 (Nov 29, 2021)

FEATURES:
* Added parsers for `crypto.com`, `coinbase pro`, and `celcius`

ENHANCEMENTS:

BUG FIXES:
* Fixed `recieve` total quantity on model

---

## 0.18.0 (Nov 28, 2021)

FEATURES:

ENHANCEMENTS:
* Moved parsers to core, renamed, and de-coupled from django dependencies

BUG FIXES:

---

## 0.17.1 (Nov 24, 2021)

FEATURES:

ENHANCEMENTS:
* Converted coinbase importer to be more standard

BUG FIXES:
* Fixed more rounding oddness
* Fixed `./initialize.sh` to actually work

---

## 0.17.0 (Nov 24, 2021)

FEATURES:
* Added CryptKeeper csv importer
  * This is akin to a backup, export the CSV from transactions and you can import it back in on the importer page

ENHANCEMENTS:
* Fixed some decimal logic and moved validators a bit
* TODO: DFR seems to 

BUG FIXES:

Known Issues:
* DFR won't trim trailing zeros from the API and it causes so strangeness. Had to increase zeros for now.

---


## 0.16.1 (Nov 23, 2021)

FEATURES:

ENHANCEMENTS:

BUG FIXES:
* /api rooted incorrectly

---

## 0.16.0 (Nov 23, 2021)

FEATURES:
* Spot price API frontend created
* Added support for more time formats to DRF

ENHANCEMENTS:

BUG FIXES:
---

## 0.15.1 (Nov 22, 2021)

FEATURES:

ENHANCEMENTS:
* Move changelog to dedicated file
* Updated welcome page.

BUG FIXES:
---

## 0.15.0 (Nov 22, 2021)

FEATURES:
* `crypto_price_finder` added for historical price lookup, no api key required
  * Note: It is running off of coinbase's public API with throttling (around 10/second). Should be fine for light workloads
* Blockfi `blockfi_all_transactions` importer created. Should fully cover all blockfi transactions if you upload both reports

ENHANCEMENTS:
* Added better auto-detection for reports
* Expanded `notes` field to 1000 characters

BUG FIXES:
* Bad included for `dotmap` which is no longer used

---

## 0.14.0 (Nov 14, 2021)

FEATURES:
* Rename transaction fields

---

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