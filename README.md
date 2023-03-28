# Stalemate
Stalemate is a script for Chatango that logs in to your accounts to prevent them from expiration, it logs in to multiple at once and shows time taken as well as what accounts it was not able to log in to if any.

## Usage

- Install [Python 3.8.0](https://www.python.org/downloads/release/python-380/) - Recommended "Windows x86-64 executable installer"
- Select to customize your installation.
- Make sure "pip" is ticked in the `Optional Features`  
  Make sure "Add Python to environment variables" is ticked in `Advanced Options`
- Open command prompt and type `pip install websockets`, if command is not recognized try restarting your computer
- Click "<> Code" and download ZIP  
  Unzip the folder when finished downloading  
  Edit `accounts.txt` with the account details you want to log using the example format
- Double left click on `stalemate.py` to run the script
- If it immediately closes, right click `stalemate.py` and "Edit with IDLE"  
  At the top, click "Run" and "Run module" and you may see errors.

## Optional
Since you would be inputting passwords in a text file, here are suggestions to keep those passwords safe
- Hide the file in File Explorer by selecting the folder then `View` and "Hide selected items"
- Remove login data from `accounts.txt` when done
- Copy and paste the login data elsewhere

## Notice
If you do not trust this script, look at the `stalemate.py` file and read the comments in triple quotations to get an idea of what it does.
