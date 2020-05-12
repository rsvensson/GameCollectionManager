import re
import bs4
import requests
import unicodedata  # For converting '\xa0' to spaces etc

_baseURL = "https://www.mobygames.com/game/"
_titleCSS = ".niceHeaderTitle > a:nth-child(1)"  # CSS for title string
_platformCSS = ".niceHeaderTitle > small:nth-child(2) > a:nth-child(1)"  # CSS for platform string

_platforms = {  # name : url
    "Arcade": "arcade",
    # Atari
    "Atari 2600": "atari-2600", "Atari 5200": "atari-5200",
    "Atari 7800": "atari-7800", "Atari 8-bit": "atari-8-bit",
    "Atari ST": "atari-st", "Jaguar": "jaguar",
    # Commodore
    "Commodore PET//CBM": "pet", "VIC-20": "vic-20",
    "Commodore 64": "c64", "Commodore 16, Plus//4": "commodore-16-plus4",
    "Commodore 128": "c128", "Amiga": "amiga",
    # Nintendo
    "NES": "nes", "SNES": "snes", "Nintendo 64": "n64",
    "GameCube": "gamecube", "Wii": "wii", "Wii U": "wii-u",
    "Nintendo Switch": "switch",
    "Game Boy": "gameboy", "Game Boy Color": "gameboy-color",
    "Game Boy Advance": "gameboy-advance", "Nintendo DS": "nintendo-ds",
    "Nintendo DSi": "nintendo-dsi", "Nintendo 3DS": "3ds",
    "New Nintendo 3DS": "new-nintendo-3ds",
    # Sega
    "Sega Master System": "sega-master-system", "Genesis": "genesis",
    "Sega CD": "sega-cd", "Sega 32X": "sega-32x",
    "Sega Saturn": "sega-saturn", "Dreamcast": "dreamcast",
    "Game Gear": "game-gear",
    # Hudson/NEC
    "TurboGrafx-16": "turbo-grafx", "TurboGrafx CD": "turbografx-cd",
    "SuperGrafx": "supergrafx",
    # Sony
    "PlayStation": "playstation", "PlayStation 2": "ps2", "PlayStation 3": "ps3",
    "PlayStation 4": "playstation-4", "PSP": "psp", "PS Vita": "ps-vita",
    # Microsoft
    "Xbox": "xbox", "Xbox 360": "xbox360", "Xbox One": "xbox-one",
    # PC
    "Windows": "windows", "Linux": "linux", "Macintosh": "macintosh"
}


def _parseTitle(title: str) -> str:
    # Parse game name to fit Moby Games' standards for URLs

    badchars = '''!()[]{};:'"\,<>./?@#$%^&*~ōūåäö'''
    title = title.lower()  # Make lowercase
    title = title.strip()  # Remove surrounding whitespace
    temp = []
    for letter in title:  # Remove bad characters
        if letter in badchars:
            continue
        temp.append(letter)
        title = "".join(temp)
        title = title.replace(" ", "-")  # Replace spaces inside string with hyphens

    return title


def _trySuggestions(title: str, platform: str):
    # Checks if the suggested URLs match

    newtitle = ""
    pTitle = _parseTitle(title)
    res = requests.get(_baseURL + "/".join((_platforms[platform], pTitle, "release-info")))
    suggestionsCSS = ".col-md-12 > div:nth-child(3) > ul:nth-child(2)"  # List of URLs

    # Find new url
    url = re.compile(r'".*"')  # URL is located within quotation marks
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    res = soup.select(suggestionsCSS)
    if len(res) > 0:
        suggestionURLs = url.findall(res.pop().decode())
    else:
        return None

    # Try each suggestion
    for suggestion in suggestionURLs:
        # The suggestions all use the Combined View. Insert the platform into url
        temp = suggestion.strip('"').split('/')
        temp.insert(4, _platforms[platform])
        newurl = "/".join(temp)

        # Get the platform and title strings
        res = requests.get(newurl)
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        te = soup.select(_titleCSS)
        if len(te) == 0:  # This shouldn't happen but who knows
            continue
        newtitle = te[0].text.strip()
        if newtitle == title:
            return res, title
        else:
            # Try removing any weird characters from the sides of the game name:
            title = title.rstrip("\\-%$£@")
            title = title.lstrip("\\-%$£@")
            if newtitle == title:
                return res, title
            else:
                continue

    return None, title


def _tryAlternatives(title: str, platform: str):
    # Occasionally the title has a trailing '-' or '_' in the url

    pTitle = _parseTitle(title)
    tempurl = [_platforms[platform], pTitle]
    for c in ["-", "_"]:
        tempurl[1] = pTitle  # Reset pTitle
        tempurl[1] += c  # Add either - or _ to string
        res = requests.get(_baseURL + "/".join(tempurl))  # Try alternative URL
        try:
            res.raise_for_status()
        except (requests.exceptions.HTTPError):  # Not a valid page
            continue
        # Parse the html and get title and platform strings
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        te = soup.select(_titleCSS)
        pf = soup.select(_platformCSS)
        # Check if title and platform match
        if len(te) > 0 and te[0].text.strip() == title and pf[0].text.strip() == platform:
            return res
        else:
            continue

    return None


def getMobyInfo(game: str, platform: str) -> dict():
    mobyCSSData = {
        "title": "html body div#wrapper div.container div#main.row div.col-md-12.col-lg-12 div.rightPanelHeader h1.niceHeaderTitle a",
        "publisher": "#coreGameRelease > div:nth-child(2) > a:nth-child(1)",
        "developer": "#coreGameRelease > div:nth-child(4) > a:nth-child(1)",
        "release": "#coreGameRelease > div:nth-child(6) > a:nth-child(1)",
        "platforms": "#coreGameRelease > div:nth-child(8)"
    }
    pTitle = _parseTitle(game)

    # Get data
    res = requests.get(_baseURL + "/".join((_platforms[platform], pTitle, "release-info")))
    try:
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
    except (requests.exceptions.HTTPError):
        # Try the suggested results on the 404 page
        res, game = _trySuggestions(game, platform)
        if res is None:
            # Couldn't find anything. Return empty values
            return {x: "" for x in mobyCSSData.keys()}

        soup = bs4.BeautifulSoup(res.text, 'html.parser')

    for data in mobyCSSData.keys():
        pf = soup.select(_platformCSS)
        pf = pf[0].text.strip() if len(pf) > 0 else ""
        if pf != platform:
            # Try some alternative URLs
            res = _tryAlternatives(game, platform)
            if res is None:  # Nothing was found.
                return {x: "" for x in mobyCSSData.keys()}
            soup = bs4.BeautifulSoup(res.text, 'html.parser')
        temp = soup.select(mobyCSSData[data])
        try:
            if data == "platforms":
                # Make sure we don't include the '| Combined View' text
                mobyCSSData[data] = unicodedata.normalize("NFKD", temp[0].text.split("|", 1)[0].strip())
                # Also make sure to insert the platform we're looking for
                if platform not in mobyCSSData[data]:
                    mobyCSSData[data] = platform + ", " + mobyCSSData[data]
            else:
                mobyCSSData[data] = unicodedata.normalize("NFKD", temp[0].text.strip())
        except (IndexError):  # Not all games have all data
            mobyCSSData[data] = ""

    return mobyCSSData


if __name__ == "__main__":
    testGames = [("Wai Wai World 2 - SOS!! Parsley Jō", "NES"),  # 'ō' gets truncated, but is a '-' in the actual url. Found through the suggestions.
                 ("Mega Man", "NES"),  # First result is the DOS game. NES game found by the alternative URL checks.
                 ("Final Fantasy-", "NES"),  # The suggestions for this don't include the right game
                 ("Super Mario 64-", "Nintendo 64"),  # Found correctly in the suggestions
                 ("Chrono Trigger", "Nintendo DS"),
                 ("Legend of Zelda: Link's Awakening", "Game Boy"),
                 ("Silent Hill", "PlayStation"),
                 ("Fable", "Xbox"),
                 ("Final Fantasy VII", "PlayStation")]

    for game in testGames:
        data = getMobyInfo(game[0], game[1])

        for i in data:
            print(i + ":\t" + data[i])
        print()

