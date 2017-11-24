# Tab Stack List Previews for Vivaldi
This repository contains UI customizations for the Vivaldi browser to transform the tab stack previews, which by default displays as a grid, into a scrollable list. 

![Tab Stack List Preview demonstration](https://imgur.com/FQ97nAm)

## Dependencies
* Python 3.6

## How to Patch
Run the Python script `patch.py`, passing the application directory for Vivaldi. For example, on a Windows 10 system, having installed Vivaldi for the current user, the path would be `C:\Users\[your_user_name]\AppData\Local\Vivaldi\Application\`.

## Disclaimer
I make no guarantee that any of this code will work as intended. The script makes a copy of `browser.html` and `common.css` before modifying them, but it wouldn't hurt to back up these files yourself.

