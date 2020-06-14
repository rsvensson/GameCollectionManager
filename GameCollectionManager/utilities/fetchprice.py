import re
import socket
from time import sleep

import bs4
import requests
import unicodedata as ucd
from decimal import *


_baseURL = "https://www.pricecharting.com/game/"
_loosePriceCSS = "#used_price > span:nth-child(1)"
_CIBPriceCSS = "#complete_price > span:nth-child(1)"
_newPriceCSS = "#new_price > span:nth-child(1)"
_gradedPriceCSS = "#price_data > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(4) > span:nth-child(1)"
_BoxPriceCSS = "#price_data > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(5) > span:nth-child(1)"
_ManualPriceCSS = "#price_data > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(6) > span:nth-child(1)"

# Platform keys are named after what we present to the user in the platforms drop-downs in-app, not what they're
# necessarily called on Pricecharting. Some systems don't have certain regions on Pricecharting, such as PAL & JP
# regions for Atari 2600. For these we default to the US region if none other is appropriate.
_platforms = {  # Platform: [NTSC (JP), NTSC (NA), PAL]
    "NES": ("famicom", "nes", "pal-nes"),
    "Famicom Disk System": ("famicom-disk-system", "famicom-disk-system", "famicom-disk-system"),
    "SNES": ("super-famicom", "super-nintendo", "pal-super-nintendo"),
    "Nintendo 64": ("jp-nintendo-64", "nintendo-64", "pal-nintendo-64"),
    "GameCube": ("jp-gamecube", "gamecube", "pal-gamecube"),
    "Wii": ("jp-wii", "wii", "pal-wii"),
    "Wii U": ("jp-wii-u", "wii-u", "pal-wii-u"),
    "Switch": ("jp-nintendo-switch", "nintendo-switch", "pal-nintendo-switch"),
    "Game Boy": ("jp-gameboy", "gameboy", "pal-gameboy"),
    "Game Boy Color": ("jp-gameboy-color", "gameboy-color", "pal-gameboy-color"),
    "Game Boy Advance": ("jp-gameboy-advance", "gameboy-advance", "pal-gameboy-advance"),
    "Nintendo DS": ("jp-nintendo-ds", "nintendo-ds", "pal-nintendo-ds"),
    "Nintendo 3DS": ("jp-nintendo-3ds", "nintendo-3ds", "pal-nintendo-3ds"),
    "Virtual Boy": ("jp-virtual-boy", "virtual-boy", ""),
    "Game & Watch": ("game-&-watch"),
    "PlayStation": ("jp-playstation", "playstation", "pal-playstation"),
    "PlayStation 2": ("jp-playstation-2", "playstation-2", "pal-playstation-2"),
    "PlayStation 3": ("jp-playstation-3", "playstation-3", "pal-playstation-3"),
    "PlayStation 4": ("jp-playstation-4", "playstation-4", "pal-playstation-4"),
    "PSP": ("jp-psp", "psp", "pal-psp"),
    "PS Vita": ("jp-playstation-vita", "playstation-vita", "pal-playstation-vita"),
    "SEGA Master System": ("", "sega-master-system", "pal-sega-master-system"),
    "Genesis": ("jp-sega-mega-drive", "sega-genesis", "pal-sega-mega-drive"),
    "SEGA CD": ("jp-sega-mega-cd", "sega-cd", "pal-sega-mega-cd"),
    "SEGA 32X": ("jp-super-32x", "sega-32x", "pal-mega-drive-32x"),
    "SEGA Saturn": ("jp-sega-saturn", "sega-saturn", "pal-sega-saturn"),
    "Dreamcast": ("jp-sega-dreamcast", "sega-dreamcast", "pal-sega-dreamcast"),
    "Game Gear": ("jp-sega-game-gear", "sega-game-gear", "pal-sega-game-gear"),
    "SEGA Pico": ("jp-sega-pico", "sega-pico", "pal-sega-pico"),
    "Xbox": ("xbox", "xbox", "pal-xbox"),
    "Xbox 360": ("xbox-360", "xbox-360", "pal-xbox-360"),
    "Xbox One": ("xbox-one", "xbox-one", "pal-xbox-one"),
    "Atari 2600": ("atari-2600" "atari-2600", "atari-2600"),
    "Atari 5200": ("atari-5200", "atari-5200", "atari-5200"),
    "Atari 7800": ("atari-7800", "atari-7800", "atari-7800"),
    "Atari 8-bit": ("atari-400", "atari-400", "atari-400"),
    "Lynx": ("atari-lynx", "atari-lynx", "atari-lynx"),
    "Jaguar": ("jaguar", "jaguar", "jaguar"),
    "Neo Geo AES": ("neo-geo-aes", "neo-geo-aes", "neo-geo-aes"),
    "Neo Geo MVS": ("neo-geo", "neo-geo", "neo-geo"),
    "Neo Geo CD": ("neo-geo-cd", "neo-geo-cd", "neo-geo-cd"),
    "Neo Geo Pocket Color": ("neo-geo-pocket-color", "neo-geo-pocket-color", "neo-geo-pocket-color"),
    "PC": ("pc-games", "pc-games", "pc-games"),
    "3DO": ("3do", "3do", "3do"),
    "Amiga": ("amiga", "amiga", "amiga"),
    "Amiga CD32": ("amiga-cd32", "amiga-cd32", "amiga-cd32"),
    "Arcadia 2001": ("arcadia-2001", "arcadia-2001", "arcadia-2001"),
    "Bally Astrocade": ("bally-astrocade", "bally-astrocade", "bally-astrocade"),
    "CD-i": ("cd-i", "cd-i", "cd-i"),
    "Colecovision": ("colecovision", "colecovision", "colecovision"),
    "Commodore 64": ("commodore-64", "commodore-64", "commodore-64"),
    "Fairchild Channel F": ("fairchild-channel-f", "fairchild-channel-f", "fairchild-channel-f"),
    "Game.Com": ("gamecom", "gamecom", "gamecom"),
    "Intellivision": ("intellivision", "intellivision", "intellivision"),
    "Mattel Aquarius": ("mattel-aquarius", "mattel-aquarius", "mattel-aquarius"),
    "MSX": ("pal-msx", "pal-msx", "pal-msx"),
    "MSX 2": ("pal-msx2", "pal-msx2", "pal-msx2"),
    "N-Gage": ("n-gage", "n-gage", "n-gage"),
    "Pokémon Mini": ("pokemon-mini", "pokemon-mini", "pokemon-mini"),
    "TI-99/4A": ("ti-99", "ti-99", "ti-99"),
    "TurboGrafx-16": ("turbografx-16", "turbografx-16", "turbografx-16"),
    "Vectrex": ("vectrex", "vectrex", "vectrex"),
    "VIC-20": ("vic-20", "vic-20", "vic-20")
}


def _parseTitle(title: str) -> str:
    # Parse game name to fit Pricecharting's standards for URLs

    badchars = '''!()[]{};:'"\,<>./?@#$%^&*~ōūåäö°'''
    title = title.lower()  # Make lowercase
    title = title.strip()  # Remove surrounding whitespace
    title = title.replace("é", "e")  # Pricecharting uses e everywhere instead of é, i.e. Pokemon rather than Pokémon

    # Some people like to have the leading "the" after the main part of the title, e.g. "Legend of Zelda, the"
    title = title.replace(", the", "")
    temp = []
    for letter in title:  # Remove bad characters
        if letter in badchars:
            continue
        temp.append(letter)
    title = "".join(temp)
    title = title.replace(" ", "-")  # Replace spaces inside string with hyphens

    # Remove leading "the"
    if title[:4] == "the-":
        title = title[4:]

    return title


def _parsePlatform(platform: str) -> str:
    # Some substitutions for certain platforms:
    if platform.lower() in ("mega drive", "sega mega drive"):  # Because Genesis is a band not a console
        platform = "Genesis"
    elif platform.lower() == "sega dreamcast":
        platform = "Dreamcast"
    elif platform.lower() in ("sega mega cd", "mega cd"):
        platform = "Sega CD"
    elif platform.lower() in ("steam", "windows", "linux", "mac", "dos"):
        platform = "PC"
    elif platform.lower() in ("nintendo entertainment system", "famicom disk system"):
        platform = "NES"
    elif platform.lower() == "nintendo gamecube":
        platform = "GameCube"
    elif platform.lower() == "nintendo wii":
        platform = "Wii"
    elif platform.lower() == "nintendo wii u":
        platform = "Wii U"
    elif platform.lower() == "atari lynx":
        platform = "Lynx"
    elif platform.lower() == "magnavox odyssey²":
        platform = "Odyssey 2"
    elif platform.lower() == "neo geo aes":
        platform = "Neo Geo"
    elif platform.lower() == "nintendo 64dd":
        platform = "Nintendo 64"
    elif platform.lower() == "playstation portable":
        platform = "PSP"
    elif platform.lower() == "playstation vita":
        platform = "PS Vita"
    elif platform.lower() == "turbografx-16 cd":
        platform = "TurboGrafx CD"

    return platform


def _trySuggestions(platform: str, region: int, soup: bs4.BeautifulSoup) -> bs4.BeautifulSoup:
    """
    Goes through the list of games and tries to find one that matches the platform
    :param platform: The platform we're looking for
    :param region: Which region. 0: NTSC (JP), 1: NTSC (NA), 2: PAL
    :param soup: BeautifulSoup object
    :return: BeautifulSoup object for new page if found, else a NoneType BeautifulSoup object
    """

    titleUrlRegex = re.compile(r'href=\".*?\"')
    titles = soup.find_all("td", {"class": "title"})
    consoles = soup.find_all("td", {"class": "console"})
    url = ""

    for title, console in zip(titles, consoles):
        if console.text.lower().replace(" ", "-") == _platforms[platform][region]:
            url = titleUrlRegex.findall(title.decode()).pop()[5:].strip('"')
            break

    if len(url) > 0:
        res = requests.get(url)
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        return soup

    return soup.clear()

def getPriceData(title: str, platform: str, region: str, currency="USD") -> dict:
    """
    Tries to look up pricing info for a game on Pricecharting.com
    :param title: The title of the game we're looking for
    :param platform: Which platform the game is on
    :param region: Which regional release we're looking for
    :param currency: Which currency we want back. Possible options are: USD, AUD, BRL, CAD, EUR, GBP, and MXN
    :return: A dictionary with the game's current average prices (loose, cib, and new)
    """

    priceInfo = {"loose": "#used_price > span:nth-child(1)",
                 "cib": "#complete_price > span:nth-child(1)",
                 "new": "#new_price > span:nth-child(1)"}

    regions = {"NTSC (JP)": 0, "NTSC (NA)": 1, "PAL": 2}
    rates = {"USD": 1.0, "AUD": 0.0, "BRL": 0.0, "CAD": 0.0, "EUR": 0.0, "GBP": 0.0, "MXN": 0.0}
    sign = {"USD": "$", "AUD": "AUD ", "BRL": "R$", "CAD": "CAD ", "EUR": "€", "GBP": "£", "MXN": "Mex$"}
    ratesRegex = re.compile(r'("\w{3}":\d\.\d.*.)')

    pTitle = _parseTitle(title)
    pPlatform = _parsePlatform(platform)

    # Sanity check
    if region in ("PAL A", "PAL B"):
        region = "PAL"
    elif region not in ("NTSC (JP)", "NTSC (NA)", "PAL"):
        region = "NTSC (NA)"
    if pPlatform in _platforms.keys():
        fullURL = _baseURL + "/".join((_platforms[pPlatform][regions[region]], pTitle))
    else:  # Platform not supported
        return {x: "N/A" for x in priceInfo.keys()}

    # Error handling
    try:
        res = requests.get(fullURL)
    except socket.gaierror:  # Most likely no internet connection
        return {x: "N/A" for x in priceInfo.keys()}
    try:
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, "html.parser")
    except requests.exceptions.HTTPError:  # Not found
        return {x: "N/A" for x in priceInfo.keys()}
    if len(soup.select("#product_name > a:nth-child(1)")) == 0:  # Didn't find the right page, try suggestions
        soup = _trySuggestions(platform, regions[region], soup)
        if soup is None:  # Still couldn't find anything
            return {x: "N/A" for x in priceInfo.keys()}

    # Get currency rates
    currentRates = ratesRegex.findall(res.text)[0].split(",")
    for c in currentRates:
        cur, rate = c.split(":")
        rates[cur.strip('"')] = float(rate.rstrip("};"))

    for key, val in priceInfo.items():
        price = ucd.normalize("NFKD", soup.select(val)[0].text.strip()).lstrip("$")
        if price == "N/A":  # No price found
            priceInfo[key] = "N/A"
            continue
        getcontext().prec = len(price) - 1  # Dynamically set precision to 2 decimal points
        priceInfo[key] = sign[currency] + str(Decimal(price) * Decimal(rates[currency]))

    return priceInfo


if __name__ == "__main__":
    testGames = [("F-Zero", "SNES", "PAL"),
                 ("Tetris", "NES", "NTSC (NA)"),
                 ("Pokémon Shock Tetris", "Pokémon Mini", "NTSC (NA)", "EUR"),
                 ("Legend of Zelda: Link's Awakening DX", "Game Boy Color", "NTSC (NA)", "MXN"),
                 ("Legend of Zelda: Ocarina of Time", "Nintendo 64", "PAL", "GBP"),
                 ("Silent Hill", "PlayStation", "NTSC (NA)")]

    for game in testGames:
        print(game[0], ": ", getPriceData(game[0], game[1], game[2], game[3] if len(game) == 4 else "USD"))
        sleep(5)
