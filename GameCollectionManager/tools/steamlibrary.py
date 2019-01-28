from requests.exceptions import HTTPError
from steam import WebAPI


def getSteamLibrary(apiKey: str, steamID: int) -> list:
    try:
        api = WebAPI(apiKey, https=True)
    except HTTPError:
        raise PermissionError("403 Client Error: Forbidden.\nWrong API key?")
    else:
        games = api.call("IPlayerService.GetOwnedGames", steamid=steamID,
                         include_appinfo=1, include_played_free_games=1, appids_filter="name")
        if len(games["response"]) == 0:
            raise ValueError("No games found. Wrong SteamID?")
        else:
            gamelist = []
            for game in games["response"]["games"]:
                gamelist.append({"Platform": "Steam", "Name": game["name"],
                             "Region": "Steam", "Code": "",
                             "Game": "Yes", "Box": "Yes", "Manual": "Yes",
                             "Year": "", "Comment": ""})
            return gamelist


# Following doesn't work with pyinstaller. rip steamodd. fuck windows. :(
"""
import steam
from steam.api import interface


def getSteamLibrary(apiKey: str, steamID: int) -> list:
    steam.api.key.set(apiKey)
    try:
        games = interface("IPlayerService").GetOwnedGames(steamid=steamID, include_appinfo=1,
                                                          include_played_free_games=1)
        if len(games["response"]) == 0:
            raise ValueError("No games found. Wrong SteamID?")
    except steam.api.HTTPError:
        raise PermissionError("401 Unauthorized. Wrong API Key?")

    gamelist = []

    for game in games["response"]["games"]:
        gamelist.append({"Platform": "Steam", "Name": game["name"],
                         "Region": "Steam", "Code": "",
                         "Game": "Yes", "Box": "Yes", "Manual": "Yes",
                         "Year": "", "Comment": ""})

    return gamelist
"""