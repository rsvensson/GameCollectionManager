import steam
from steam.api import interface


def getSteamLibrary(apiKey: str, steamID: int) -> list:
    # TODO: Error handling
    steam.api.key.set(apiKey)
    games = interface("IPlayerService").GetOwnedGames(steamid=steamID, include_appinfo=1,
                                                      include_played_free_games=1)
    gamelist = []

    for game in games["response"]["games"]:
        gamelist.append({"Platform": "Steam", "Name": game["name"],
                         "Region": "Steam", "Code": "",
                         "Game": "Yes", "Box": "Yes", "Manual": "Yes",
                         "Year": "", "Comment": ""})

    return gamelist
