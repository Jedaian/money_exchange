# money_exchange
Simple Python program for a friend's money exchanger shop

## Install on MacOS
pyinstaller --onefile --windowed --icon=assets/icon.ico --add-data "db/database.db:db" main.py

## Install on Windows
pyinstaller --onefile --windowed --icon=assets/icon.ico --add-data "db/database.db;db" main.py
