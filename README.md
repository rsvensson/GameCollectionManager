# GameCollectionManager
Game Collection Manager using QT for Python

## Features
* Search/filter your library
* Import Steam library
* Import platform template
* Auto-fill missing info
* Export library to CSV
* Library overview/stats
* Game randomizer

## Usage
A default collection is included. To start from scratch, just delete 'collection.db' in data/db and the application will create an empty database on startup.
To import games either use 'Add to collection' to add a single item (game/console/accessory), 'Import Steam Library, or 'Import platform template' to import all the games from selected platforms and check the boxes of the games you own.
### Tab views
* Overview - Shows an overview of the number of items for each platform.
* Games/Consoles/Accessories - Tables of the items in your collection. Highlight a cell and press Enter to start editing it, or just start typing with a cell highlighted. Double clicking a row opens up a details side-panel, which shows the game's cover image and details organized. If any info is missing you can use the _Fetch missing info_ button to try to fill in any missing info automatically, including the cover image. Afterwards you can click the _Save_ button to save this to the database.
* Randomizer - This tab selects a random game from your collection. The idea is that if you can't decide what to play, this will decide for you. Select the platforms and/or genres you want to randomize from and click 'Randomize'.
### Adding items to collection
* Add to collection - Adds a single item to the collection. Select item type (game/console/accessory) and platform, and enter the information for the item. You can click the _Autofill_ button after entering the name and platform, and optionally a country, to fill in the rest of the info automatically.
* Import Steam library - This allows you to import your Steam library into GCM. You need a Steam Web API key (https://steamcommunity.com/dev/apikey) as well as your SteamID.
* Import platform template - When importing a platform template, all games for the selected platforms are imported (or at least most; some platforms aren't quite complete) but neither the 'Game', 'Box' or 'Manual' checkboxes are checked. These games are treated as not being part of your collection. To show them, untick the checkbox under 'View->Hide games not in collection'. To add games from the template, simply check the checkboxes of the games you own. When you're done, use 'View->Remove items not in collection' to remove unchecked items. This might help speed things up if you have a lot of games to enter. Afterwards you can then either enter more info for each game manually, or try using the auto-fill feature of the side-panel.
### Export collection to CSV
Choose which tables you want to export and the filetype. Possible filetypes are csv (comma-separated values) and tsv (tab-separated values). The resulting files will be put in the GameCollectionManager folder.

## Dependencies
* PySide2
* Matplotlib
* Numpy
* Requests
* python-steam (https://github.com/ValvePython/steam)

To make a Windows binary, install the above dependencies using pip, as well as PyInstaller. You also need 7zip installed. Then run 'tools/buildforwindows.ps1' from the project root in a PowerShell window. A .7z file will be created in the 'output' directory.
