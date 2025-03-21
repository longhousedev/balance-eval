import argparse
import random
import pathlib

# TAG Configuration Files

config = {
    "nPlayers" : 2,
    "mode" : "exhaustive",
    "matchups" : 10,
    "verbpathlib.Pathe" : false,
}

params = {}
listener = {}

osla_player = {
    "class":"players.simple.OSLAHeuristic",
    "heuristic" : {
        "class" : "players.heuristics.ScoreHeuristic"
    }
}

random_player = {
      "class" : "players.simple.RandomPlayer"
}

##########################
# Dominion Configuration #
##########################

# Good Dominion Player

# Mid Dominion Player


# Dominion Listener

dominion_listener = {
    "class": "evaluation.listeners.MetricsGameListener",
    "args": [
      {"enum" : "evaluation.metrics.IDataLogger$ReportDestination", "value" : "ToFile"},
      [
        {"enum" : "evaluation.metrics.IDataLogger$ReportType", "value" : "RawDataPerEvent"}
      ],
      [
      {
        "class" : "games.dominion.metrics.DominionMetrics$ChosenParams"
      },
      {
        "class": "evaluation.metrics.GameMetrics$Winner"
      }      
    ]
    ]
}

# Dominion cards
dominion_cards: set[str] = {
    "CELLAR",
    "CHAPEL",
    "MOAT",
    "HARBINGER",
    "MERCHANT",
    "VASSAL",
    "VILLAGE",
    "WORKSHOP",
    "BUREAUCRAT",
    "GARDENS",
    "MILITIA",
    "MONEYLENDER",
    "POACHER",
    "REMODEL",
    "SMITHY",
    "THRONE_ROOM",
    "BANDIT",
    "COUNCIL_ROOM",
    "FESTIVAL",
    "LABORATORY",
    "LIBRARY",
    "MARKET",
    "MINE",
    "SENTRY",
    "WITCH",
    "ARTISAN"
}
    
def populate_dominion_params():
    """
    Populate the params dictionary with the Dominion game parameters.
    """
    params["HAND_SIZE"] = random.choice([3,5,7,10])
    params["PILES_EXHAUSTED_FOR_GAME_END"] = random.choice([1,3,5,7,10])
    params["KINGDOM_CARDS_OF_EACH_TYPE"] = random.choice([5, 10, 15, 20])
    params["CURSE_CARDS_PER_PLAYER"] = random.choice([5, 10, 15, 20])
    params["STARTING_COPPER"] = random.choice([3,5,7,10,15])
    params["STARTING_ESTATES"] = random.choice([1,3,5,7,10])
    params["COPPER_SUPPLY"] = random.choice([10,20,32,40,50])
    params["SILVER_SUPPLY"] = random.choice([10,20,30,40,50])
    params["GOLD_SUPPLY"] = random.choice([10,20,30,40,50])
    params["CARDS"] = random.sample(dominion_cards, 10)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process a file path and a number.")
    parser.add_argument("game", type=str, help="The game to play")
    parser.add_argument("folder", type=str, help="The name of the output folder")
    
    # Game specific configuration
    match parser.game:
        case "Dominion":
            populate_dominion_params()
            listener = dominion_listener
        case _:
            print("Game not supported")
            exit(1)
    
    # create directories
    pathlib.Path.mkdir(folder)
    pathlib.Path.mkdir(folder + "/players")
    pathlib.Path.mkdir(folder + "/listener")
    pathlib.Path.mkdir(folder + "/output")
    pathlib.Path.mkdir(folder + "/gameParams")
    
    # Populate configuration file with these directories
    config["palyerDirectory"] = folder + "/players"
    config["listener"] = folder + "/listener"
    config["destDir"] = folder + "/output"
    config["gameParams"] = folder + "/gameParams" + "/gameParams.json"
    
    # Write configuration files to json