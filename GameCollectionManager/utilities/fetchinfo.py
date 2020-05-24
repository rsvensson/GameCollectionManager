import re
import unicodedata as ucd  # For converting '\xa0' to spaces etc

import bs4
import requests

_baseURL = "https://www.mobygames.com/game/"
_titleCSS = ".niceHeaderTitle > a:nth-child(1)"  # CSS for title string
_platformCSS = ".niceHeaderTitle > small:nth-child(2) > a:nth-child(1)"  # CSS for platform string

_platforms = {  # Name: URL
    '1292 Advanced Programmable Video System': '1292-advanced-programmable-video-system',
    '3DO': '3do',
    'APF MP1000/Imagination Machine': 'apf',
    'Acorn 32-bit': 'acorn-32-bit',
    'Adventure Vision': 'adventure-vision',
    'Alice 32/90': 'alice-3290',
    'Altair 680': 'altair-680',
    'Altair 8800': 'altair-8800',
    'Amazon Alexa': 'amazon-alexa',
    'Amiga': 'amiga',
    'Amiga CD32': 'amiga-cd32',
    'Amstrad CPC': 'cpc',
    'Amstrad PCW': 'amstrad-pcw',
    'Android': 'android',
    'Apple I': 'apple-i',
    'Apple II': 'apple2',
    'Apple IIgs': 'apple2gs',
    'Arcade': 'arcade',
    'Arcadia 2001': 'arcadia-2001',
    'Arduboy': 'arduboy',
    'Astral 2000': 'astral-2000',
    'Atari 2600': 'atari-2600',
    'Atari 5200': 'atari-5200',
    'Atari 7800': 'atari-7800',
    'Atari 8-bit': 'atari-8-bit',
    'Atari ST': 'atari-st',
    'Atom': 'atom',
    'BBC Micro': 'bbc-micro_',
    'BREW': 'brew',
    'Bally Astrocade': 'bally-astrocade',
    'BeOS': 'beos',
    'BlackBerry': 'blackberry',
    'Blu-ray Disc Player': 'blu-ray-disc-player',
    'Browser': 'browser',
    'Bubble': 'bubble',
    'CD-i': 'cd-i',
    'CDTV': 'cdtv',
    'CP/M': 'cpm',
    'Camputers Lynx': 'camputers-lynx',
    'Casio Loopy': 'casio-loopy',
    'Casio PV-1000': 'casio-pv-1000',
    'Channel F': 'channel-f',
    'ClickStart': 'clickstart',
    'Coleco Adam': 'colecoadam',
    'ColecoVision': 'colecovision',
    'Colour Genie': 'colour-genie',
    'Commodore 128': 'c128',
    'Commodore 16, Plus/4': 'commodore-16-plus4',
    'Commodore 64': 'c64',
    'Commodore PET/CBM': 'pet',
    'Compal 80': 'compal-80',
    'Compucolor I': 'compucolor-i',
    'Compucolor II': 'compucolor-ii',
    'Compucorp Programmable Calculator': 'compucorp-programmable-calculator',
    'CreatiVision': 'creativision',
    'DOS': 'dos',
    'DVD Player': 'dvd-player',
    'Dedicated console': 'dedicated-console',
    'Dedicated handheld': 'dedicated-handheld',
    'Didj': 'didj',
    'DoJa': 'doja',
    'Dragon 32/64': 'dragon-3264',
    'Dreamcast': 'dreamcast',
    'ECD Micromind': 'ecd-micromind',
    'Electron': 'electron',
    'Enterprise': 'enterprise',
    'Epoch Cassette Vision': 'epoch-cassette-vision',
    'Epoch Game Pocket Computer': 'epoch-game-pocket-computer',
    'Epoch Super Cassette Vision': 'epoch-super-cassette-vision',
    'ExEn': 'exen',
    'Exelvision': 'exelvision',
    'Exidy Sorcerer': 'exidy-sorcerer',
    'FM Towns': 'fmtowns',
    'FM-7': 'fm-7',
    'FRED/COSMAC': 'fred-cosmac',
    'Fire OS': 'fire-os',
    'Freebox': 'freebox',
    'GIMINI': 'gimini',
    'GNEX': 'gnex',
    'GP2X': 'gp2x',
    'GP2X Wiz': 'gp2x-wiz',
    'GP32': 'gp32',
    'GVM': 'gvm',
    'Galaksija': 'galaksija',
    'Game Boy': 'gameboy',
    'Game Boy Advance': 'gameboy-advance',
    'Game Boy Color': 'gameboy-color',
    'Game Gear': 'game-gear',
    'Game Wave': 'game-wave',
    'Game.Com': 'game-com',
    'GameCube': 'gamecube',
    'GameStick': 'gamestick',
    'Genesis': 'genesis',
    'Gizmondo': 'gizmondo',
    'Glulx': 'glulx',
    'HD DVD Player': 'hd-dvd-player',
    'HP 9800': 'hp-9800',
    'HP Programmable Calculator': 'hp-programmable-calculator',
    'Heath/Zenith H8/H89': 'heathzenith',
    'Heathkit H11': 'heathkit-h11',
    'Hitachi S1': 'hitachi-s1',
    'Hugo': 'hugo',
    'HyperScan': 'hyperscan',
    'IBM 5100': 'ibm-5100',
    'Ideal-Computer': 'ideal-computer',
    'Intel 8008': 'intel-8008',
    'Intel 8080': 'intel-8080',
    'Intellivision': 'intellivision',
    'Interton Video 2000': 'interton-video-2000',
    'J2ME': 'j2me',
    'Jaguar': 'jaguar',
    'Jolt': 'jolt',
    'Jupiter Ace': 'jupiter-ace',
    'KIM-1': 'kim-1',
    'Kindle Classic': 'kindle',
    'Laser 200': 'laser200',
    'LaserActive': 'laseractive',
    'LeapFrog Explorer': 'leapfrog-explorer',
    'LeapTV': 'leaptv',
    'Leapster': 'leapster',
    'Linux': 'linux',
    'Lynx': 'lynx',
    'MOS Technology 6502': 'mos-technology-6502',
    'MRE': 'mre',
    'MSX': 'msx',
    'Macintosh': 'macintosh',
    'Maemo': 'maemo',
    'Mainframe': 'mainframe',
    'Mattel Aquarius': 'mattel-aquarius',
    'MeeGo': 'meego',
    'Memotech MTX': 'memotech-mtx',
    'Microbee': 'microbee',
    'Microtan 65': 'microtan-65',
    'Microvision': 'microvision',
    'Mophun': 'mophun',
    'Motorola 6800': 'motorola-6800',
    'Motorola 68k': 'motorola-68k',
    'N-Gage': 'ngage',
    'N-Gage (service)': 'ngage2',
    'NES': 'nes',
    'Nascom': 'nascom',
    'Neo Geo': 'neo-geo',
    'Neo Geo CD': 'neo-geo-cd',
    'Neo Geo Pocket': 'neo-geo-pocket',
    'Neo Geo Pocket Color': 'neo-geo-pocket-color',
    'Neo Geo X': 'neo-geo-x',
    'New Nintendo 3DS': 'new-nintendo-3ds',
    'NewBrain': 'newbrain',
    'Newton': 'newton',
    'Nintendo 3DS': '3ds',
    'Nintendo 64': 'n64',
    'Nintendo DS': 'nintendo-ds',
    'Nintendo DSi': 'nintendo-dsi',
    'Nintendo Switch': 'switch',
    'North Star': 'northstar',
    'Noval 760': 'noval-760',
    'Nuon': 'nuon',
    'OS/2': 'os2',
    'Oculus Go': 'oculus-go',
    'Oculus Quest': 'oculus-quest',
    'Odyssey': 'odyssey',
    'Odyssey 2': 'odyssey-2',
    'Ohio Scientific': 'ohio-scientific',
    'OnLive': 'onlive',
    'Orao': 'orao',
    'Oric': 'oric',
    'Ouya': 'ouya',
    'PC Booter': 'pc-booter',
    'PC-6001': 'pc-6001',
    'PC-8000': 'pc-8000',
    'PC-88': 'pc88',
    'PC-98': 'pc98',
    'PC-FX': 'pc-fx',
    'PS Vita': 'ps-vita',
    'PSP': 'psp',
    'Palm OS': 'palmos',
    'Philips VG 5000': 'philips-vg-5000',
    'Photo CD': 'photocd',
    'Pippin': 'pippin',
    'PlayStation': 'playstation',
    'PlayStation 2': 'ps2',
    'PlayStation 3': 'ps3',
    'PlayStation 4': 'playstation-4',
    'Playdia': 'playdia',
    'Pokémon Mini': 'pokemon-mini',
    'Pokitto': 'pokitto',
    'Poly-88': 'poly-88',
    'RCA Studio II': 'rca-studio-ii',
    'Roku': 'roku',
    'SAM Coupé': 'sam-coup',
    'SC/MP': 'scmp',
    'SD-200/270/290': 'sd-200270290',
    'SEGA 32X': 'sega-32x',
    'SEGA CD': 'sega-cd',
    'SEGA Master System': 'sega-master-system',
    'SEGA Pico': 'sega-pico',
    'SEGA Saturn': 'sega-saturn',
    'SG-1000': 'sg-1000',
    'SK-VM': 'sk-vm',
    'SMC-777': 'smc-777',
    'SNES': 'snes',
    'SRI-500/1000': 'sri-5001000',
    'SWTPC 6800': 'swtpc-6800',
    'Sharp MZ-80B/2000/2500': 'sharp-mz-80b20002500',
    'Sharp MZ-80K/700/800/1500': 'sharp-mz-80k7008001500',
    'Sharp X1': 'sharp-x1',
    'Sharp X68000': 'sharp-x68000',
    'Sharp Zaurus': 'sharp-zaurus',
    'Signetics 2650': 'signetics-2650',
    'Sinclair QL': 'sinclair-ql',
    'Sol-20': 'sol-20',
    'Sord M5': 'sord-m5',
    'Spectravideo': 'spectravideo',
    'Stadia': 'stadia',
    "Super A'can": 'super-acan',
    'SuperGrafx': 'supergrafx',
    'Supervision': 'supervision',
    'Symbian': 'symbian',
    'TADS': 'tads',
    'TI Programmable Calculator': 'ti-programmable-calculator',
    'TI-99/4A': 'ti-994a',
    'TIM': 'tim',
    'TRS-80': 'trs-80',
    'TRS-80 CoCo': 'trs-80-coco',
    'TRS-80 MC-10': 'trs-80-mc-10',
    'Taito X-55': 'taito-x-55',
    'Tatung Einstein': 'tatung-einstein',
    'Tektronix 4050': 'tektronix-4050',
    'Tele-Spiel ES-2201': 'tele-spiel',
    'Telstar Arcade': 'telstar-arcade',
    'Terminal': 'terminal',
    'Thomson MO': 'thomson-mo',
    'Thomson TO': 'thomson-to',
    'Tiki 100': 'tiki-100',
    'Timex Sinclair 2068': 'timex-sinclair-2068',
    'Tizen': 'tizen',
    'Tomahawk F1': 'tomahawk-f1',
    'Tomy Tutor': 'tomy-tutor',
    'TurboGrafx CD': 'turbografx-cd',
    'TurboGrafx-16': 'turbo-grafx',
    'V.Flash': 'vflash',
    'V.Smile': 'vsmile',
    'VIC-20': 'vic-20',
    'VIS': 'vis',
    'Vectrex': 'vectrex',
    'VideoBrain': 'videobrain',
    'Videopac+ G7400': 'videopac-g7400',
    'Virtual Boy': 'virtual-boy',
    'WIPI': 'wipi',
    'Wang 2200': 'wang2200',
    'Wii': 'wii',
    'Wii U': 'wii-u',
    'Windows': 'windows',
    'Windows 3.x': 'win3x',
    'Windows Apps': 'windows-apps',
    'Windows Mobile': 'windowsmobile',
    'Windows Phone': 'windows-phone',
    'WonderSwan': 'wonderswan',
    'WonderSwan Color': 'wonderswan-color',
    'XaviXPORT': 'xavixport',
    'Xbox': 'xbox',
    'Xbox 360': 'xbox360',
    'Xbox One': 'xbox-one',
    'Xerox Alto': 'xerox-alto',
    'Z-machine': 'z-machine',
    'ZX Spectrum': 'zx-spectrum',
    'ZX Spectrum Next': 'zx-spectrum-next',
    'ZX80': 'zx80',
    'ZX81': 'zx81',
    'Zeebo': 'zeebo',
    'Zilog Z80': 'z80',
    'Zilog Z8000': 'zilog-z8000',
    'Zodiac': 'zodiac',
    'Zune': 'zune',
    'bada': 'bada',
    'digiBlast': 'digiblast',
    'iPad': 'ipad',
    'iPhone': 'iphone',
    'iPod Classic': 'ipod-classic',
    'tvOS': 'tvos',
    'watchOS': 'watchos',
    'webOS': 'webos'
}


def _parseTitle(title: str) -> str:
    # Parse game name to fit Moby Games' standards for URLs

    badchars = '''!()[]{};:'"\,<>./?@#$%^&*~ōūåäöé'''
    title = title.lower()  # Make lowercase
    title = title.strip()  # Remove surrounding whitespace
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


def _trySuggestions(title: str, platform: str):
    # Checks if the suggested URLs match

    pTitle = _parseTitle(title)
    res = requests.get(_baseURL + "/".join((_platforms[platform], pTitle, "release-info")))
    suggestionsCSS = ".col-md-12 > div:nth-child(3) > ul:nth-child(2)"  # List of URLs
    alternativeTitlesCSS = [".col-md-8 > ul:nth-child(17)",
                            ".col-md-8 > ul:nth-child(18)",
                            ".col-md-8 > ul:nth-child(19)",  # List of alternative titles
                            ".col-md-8 > ul:nth-child(20)",  # Not all of them might be valid,
                            ".col-md-8 > ul:nth-child(21)",  # but I've seen 17, 19, 20, 25, 28 and 30 being used
                            ".col-md-8 > ul:nth-child(22)",
                            ".col-md-8 > ul:nth-child(23)",
                            ".col-md-8 > ul:nth-child(24)",
                            ".col-md-8 > ul:nth-child(25)",
                            ".col-md-8 > ul:nth-child(26)",
                            ".col-md-8 > ul:nth-child(27)",
                            ".col-md-8 > ul:nth-child(28)",
                            ".col-md-8 > ul:nth-child(29)",
                            ".col-md-8 > ul:nth-child(30)",
                            ".col-md-8 > ul:nth-child(31)"]

    # Find new url
    url = re.compile(r'".*"')  # URL is located within quotation marks
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    res = soup.select(suggestionsCSS)
    if len(res) > 0:
        suggestionURLs = [u.strip('"') for u in url.findall(res.pop().decode())]
    else:  # No suggestions found
        return None, title

    # Try each suggestion
    for suggestion in suggestionURLs:
        # The suggestions all use the Combined View. Insert the platform into url
        temp = suggestion.split("/")
        temp.insert(4, _platforms[platform])
        temp.append("release-info")
        newurl = "/".join(temp)

        # Get the platform and title strings
        res = requests.get(newurl)
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        te = soup.select(_titleCSS)
        pf = soup.select(_platformCSS)

        if len(te) == 0 or len(pf) == 0:  # This shouldn't happen but who knows
            continue
        if pf[0].text.strip() != platform:
            continue  # Not the right platform, abort

        newtitle = te[0].text.strip()
        if newtitle.lower() == title.lower():
            return res, title, newurl
        else:
            # Try removing any weird characters from the sides of the game name:
            t = title.rstrip("\\-%$£@")
            t = t.lstrip("\\-%$£@")
            if newtitle.lower() == t.lower():
                return res, t
            else:
                # Check the alternative titles (Japanese games often have different titles for example)
                alturl = newurl.split("/")
                alturl = "/".join(alturl[:-1])  # Remove the 'release-info' part. Alt titles are on the main page.
                altres = requests.get(alturl)
                soup = bs4.BeautifulSoup(altres.text, "html.parser")

                temp = []
                for alt in alternativeTitlesCSS:
                    # Try to find the alt titles
                    temp = soup.select(alt)
                    if len(temp) > 0:
                        break
                if len(temp) == 0:  # Still nothing, give up
                    continue

                altTitles = [t.strip('"') for t in url.findall(temp[0].text)]  # Not URLs but regex rule is the same
                for alt in altTitles:
                    if alt.lower() == title.lower():
                        return res, title, newurl
                    elif alt.lower() == t.lower():
                        return res, t, newurl
                    # Sometimes ō is transliterated as ou or oo
                    elif alt.lower() == title.replace("ō", "ou").lower() or\
                            alt.lower() == title.replace("ō", "oo").lower():
                        return res, title, newurl
                    elif alt.lower() == t.replace("ō", "ou").lower() or\
                            alt.lower() == t.replace("ō", "oo").lower():
                        return res, t, newurl
                    else:
                        continue

    return None, title, ""


def _tryAlternatives(title: str, platform: str):
    # Occasionally the title has a trailing '-', '_', or rarely '__' in the url

    pTitle = _parseTitle(title)
    testurl = [_platforms[platform], pTitle, "release-info"]
    for c in ["-", "_", "__"]:
        testurl[1] = pTitle  # Reset pTitle
        testurl[1] += c  # Add either '-', '_', or '__' to string
        res = requests.get(_baseURL + "/".join(testurl))  # Try alternative URL
        try:
            res.raise_for_status()
        except requests.exceptions.HTTPError:  # Not a valid page
            continue
        # Parse the html and get title and platform strings
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        te = soup.select(_titleCSS)
        pf = soup.select(_platformCSS)
        if len(te) == 0 or len(pf) == 0:
            continue

        # Check if title and platform match
        if te[0].text.strip().lower() == title.lower() and pf[0].text.strip().lower() == platform.lower():
            return res, _baseURL + "/".join(testurl)
        else:
            continue

    return None, ""


def getMobyInfo(title: str, platform: str) -> dict:
    """Takes a game name and its platform, and returns a dictionary with the game's
       information from MobyGames.com.
       :param title: Title of the game
       :param platform: The game's platform
       :return: Dictionary of the game's info
    """

    mobyCSSData = {
        "title": "html body div#wrapper div.container div#main.row div.col-md-12.col-lg-12 div.rightPanelHeader "
                 "h1.niceHeaderTitle a",
        "publisher": "#coreGameRelease > div:nth-child(2) > a:nth-child(1)",
        "developer": "#coreGameRelease > div:nth-child(4) > a:nth-child(1)",
        "release": "#coreGameRelease > div:nth-child(6) > a:nth-child(1)",
        "platforms": "#coreGameRelease > div:nth-child(8)",
        "genre": "#coreGameGenre > div:nth-child(1) > div:nth-child(2)",
    }
    pTitle = _parseTitle(title)

    # Some substitutions for certain platforms:
    if platform.lower() == "game & watch":
        title = "Game & Watch Wide Screen: " + title  # TODO: Need to figure out something better for each variety
        platform = "Dedicated handheld"
    elif platform.lower() == "mega drive":  # Because Genesis is a band not a console
        platform = "Genesis"
    elif platform.lower() == "steam":
        platform = "Windows"  # Well it could be Linux or Mac as well but...

    # Get data
    fullURL = _baseURL + "/".join((_platforms[platform], pTitle, "release-info"))
    res = requests.get(fullURL)
    try:
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
    except requests.exceptions.HTTPError:
        # Try the suggested results on the 404 page
        res, title, fullURL = _trySuggestions(title, platform)
        if res is None:
            # Couldn't find anything. Return empty values
            return {x: "" for x in mobyCSSData.keys()}

        soup = bs4.BeautifulSoup(res.text, 'html.parser')

    for key in mobyCSSData.keys():
        pf = soup.select(_platformCSS)
        pf = pf[0].text.strip() if len(pf) > 0 else ""
        if pf.lower() != platform.lower():
            # Try some alternative URLs
            res, fullURL = _tryAlternatives(title, platform)
            if res is None:  # Nothing was found.
                return {x: "" for x in mobyCSSData.keys()}
            soup = bs4.BeautifulSoup(res.text, 'html.parser')
        try:
            temp = soup.select(mobyCSSData[key])
            if key == "platforms":
                # Make sure we don't include the '| Combined View' text
                mobyCSSData[key] = ucd.normalize("NFKD", temp[0].text.split("|", 1)[0].strip())
                # Also make sure to insert the platform we're looking for
                if platform not in mobyCSSData[key]:
                    mobyCSSData[key] = platform + ", " + mobyCSSData[key]
            else:
                mobyCSSData[key] = ucd.normalize("NFKD", temp[0].text.strip())
        except IndexError:  # Not all games have all data. Just add an empty string instead.
            if key == "genre":
                # If there's an ESRB rating it takes the place of the normal genre position
                altGenreCSS = "#coreGameGenre > div:nth-child(2) > div:nth-child(4) > a:nth-child(1)"
                try:
                    temp = soup.select(altGenreCSS)
                    mobyCSSData[key] = ucd.normalize("NFKD", temp[0].text.strip())
                except IndexError:  # Still nothing
                    mobyCSSData[key] = ""
            else:
                mobyCSSData[key] = ""

    # Get release info
    releases = {}
    info = soup.find_all("div", {"class": "floatholder relInfo"})
    release = ""
    for i in info:
        titles = i.find_all("div", {"class": "relInfoTitle"})
        details = i.find_all("div", {"class": "relInfoDetails"})

        for title, detail in zip(titles, details):
            if title.text.strip() in ("Country", "Countries"):  # Make the country name the dict key
                temprelease = detail.text.split(",")
                temprelease = [x.strip() for x in temprelease]
                release = tuple(temprelease)
                releases[release] = []
            else:  # Add the rest of the info to the country name key
                releases[release].append([ucd.normalize("NFKD", title.text.strip()),
                                          ucd.normalize("NFKD", detail.text.strip())])
    mobyCSSData["releases"] = releases

    # Get cover image
    imgurlReg = re.compile(r'href=\".*?\"')
    coverURL = fullURL.replace("release-info", "cover-art")
    coverRes = requests.get(coverURL)
    coverSoup = bs4.BeautifulSoup(coverRes.text, "html.parser")
    coverReleases = coverSoup.find_all("table", {"summary": "Description of Covers"})
    coverMedia = coverSoup.find_all("div", {"class": "thumbnail"})

    # Find the "Front Cover" URLs
    coverURLs = []
    for media in coverMedia:
        covers = media.find_all("a", {"class": "thumbnail-cover"})
        for cover in covers:
            if str(cover).find("Front Cover") != -1:
                # Find 'href=' part, split at '=', and strip away '"' on the right side
                coverURLs.append(imgurlReg.findall(str(cover)).pop().split('=')[1].strip('"'))

    if len(coverURLs) == 0:  # No covers found, default to title screen shot
        imgurlReg = re.compile(r'src=\".*?\"')
        image = soup.find_all("div", {"id": "coreGameCover"})
        temp = []
        for i in image.pop().decode():
            temp.append(i)
        imgsrc = imgurlReg.findall("".join(temp)).pop().split('=')[1].strip('"')  # Find 'src=' part, then split at '='

        mobyCSSData["covers"] = {"United States": "https://www.mobygames.com" + imgsrc}
    else:
        covers = {}
        for release, url in zip(coverReleases, coverURLs):
            rel = release.find_all("td")
            for j, r in enumerate(rel):  # Find index of countries list
                if len(rel) > 9:
                    continue  # Skips player's choice releases etc (anything that has a "Package Comments" section)
                if r.text in ("Country", "Countries"):
                    # Country as key, url as value. When several countries the last ones are separated with " and ".
                    covers[rel[j+2].text.replace(" and ", " , ")] = url
                    break

        mobyCSSData["covers"] = covers

    return mobyCSSData


def getMobyRelease(name: str, platform: str, region: str, country: str = ""):
    """
    Finds a specific release for a game on MobyGames.com
    :param name: The name of the game
    :param platform: The game's platform
    :param region: The game's region (NTSC (JP), NTSC (NA), PAL accepted)
    :param country: Optionally specify a specific country
    :return: Dictionary of the release info
    """

    releaseInfo = {"publisher": "", "developer": "", "platforms": "",
                   "genre": "", "code": "", "year": ""}

    regionDict = {"NTSC (JP)": ("Japan", "Worldwide"),
                  "NTSC (NA)": ("United States", "Canada", "Worldwide"),
                  "PAL": ("United Kingdom", "Ireland", "Germany", "France", "Italy",
                          "Austria", "Belgium", "The Netherlands", "Portugal",
                          "Spain", "Switzerland", "Russia",
                          "Sweden", "Denmark", "Norway", "Finland",
                          "Australia, New Zealand", "Worldwide")}
    if region in ("PAL A", "PAL B"):
        region = "PAL"
    if region == "Steam":
        region = "NTSC (NA)"
    regionValue = regionDict[region]
    info = getMobyInfo(name, platform)

    if info["title"] == "":
        # No data found, return empty values
        return releaseInfo

    publisher = info["publisher"]
    developer = info["developer"]
    platforms = info["platforms"]
    genre = info["genre"]
    covers = info["covers"]
    yearFormat = re.compile(r"\d{4}")
    code = ""
    year = ""

    # Try to get product code, and also year since it might be different between releases
    correctRelease = ""
    for release, details in zip(info["releases"].keys(), info["releases"].values()):
        # Optionally check the specific country's release, but only if it makes sense
        # (e.g. don't check for Norway if region == NTSC (JP)
        if country != "" and country in regionValue and country in release:
            correctRelease = release
        else:
            if region == "PAL" and "United Kingdom" in release:
                # Make UK release default for PAL
                correctRelease = release
            else:
                if country == "" and correctRelease == "":
                    # UK not found, or region isn't PAL, try to find another release
                    for r in release:
                        if r in regionValue or r == regionValue:
                            correctRelease = release
                            break
                elif country != "" and correctRelease == "":
                    continue

        if correctRelease != "":
            for d in details:
                if d[0] in ("Company Code", "Nintendo Media PN", "Sony PN"):
                    code = d[1]
                elif d[0] == "Release Date":
                    year = yearFormat.findall(d[1])[0]

        if code != "" and year != "":
            break

    # Try with EAN-13 or UPC-A for the code as a fallback
    if code == "" and correctRelease != "":
        for d in info["releases"][correctRelease]:
            if d[0] in ("EAN-13", "UPC-A"):
                code = d[0] + ": " + d[1]
                break

    # Find the release's cover image
    if len(covers) > 0 and str(list(covers.values())[0]).find("/shots") == -1:
        # We have a cover image, determine region
        res = None
        for cover in covers:
            countries = cover.split(" , ")
            for country in countries:
                if region == "PAL" and country.strip() == "United Kingdom":
                    # Default to UK for PAL region
                    res = requests.get(covers[cover])
                    break
                elif country.strip() in regionValue:
                    res = requests.get(covers[cover])
                    break
            if res is not None:
                break

        if res is None:  # Correct region not found, select the first one.
            res = requests.get(list(covers.values())[0])

        imgCSS = ".img-responsive"
        imgURLReg = re.compile(r'src=\".*?\"')
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        imgURL = "https://www.mobygames.com" + imgURLReg.findall(str(soup.select(imgCSS))).pop().split('=')[1].strip('"')

    elif len(covers) > 0 and str(list(covers.values())[0]).find("/shots/") != -1:
        # Cover image wasn't found but we have a screen shot
        imgURL = list(covers.values())[0]
    else:
        # No image found
        imgURL = ""

    releaseInfo = {"publisher": publisher, "developer": developer, "platforms": platforms,
                   "genre": genre, "image": imgURL, "code": code, "year": year}
    return releaseInfo


def printInfo(info: dict):
    # Print out the info with pretty formatting
    for i in info:
        if i == "releases":
            releases = info[i].keys()
            details = info[i].values()
            print("====================================\n\n")
            print("====================================")
            print("Releases:")
            print("====================================")
            for release, detail in zip(releases, details):
                print(", ".join(release) + ":")
                print("------------------------------------")
                for d in detail:
                    print(d[0] + ":\t\t\t\t" + d[1] if len(d[0]) < 7
                          else d[0] + ":\t" + d[1] if len(d[0]) > 16
                          else d[0] + ":\t\t" + d[1])
                print("====================================")
        else:
            print(i + ":\t\t\t" + info[i] if i == "title" or i == "genre" else i + ":\t\t" + info[i])
    print()


if __name__ == "__main__":
    testGames = [("Wai Wai World 2 - SOS!! Parsley Jō", "NES"),
                 # 'ō' gets truncated, but is a '-' in the actual url. Found through the suggestions.
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

        printInfo(data)
