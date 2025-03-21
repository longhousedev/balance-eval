import argparse
import random
import pathlib
import json

# TAG Configuration Files

config = {
    "nPlayers" : 2,
    "mode" : "exhaustive",
    "matchups" : 10,
    "verbpathlib.Pathe" : False,
}

params = {}
listener = {}
elite_player = {}
good_player = {}

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

dominion_elite = {
    "budgetType" : "BUDGET_TIME",
    "rolloutLengthPerPlayer" : True,
    "rolloutTermination" : "END_TURN", 
    "rolloutLength" : 300,
    "opponentTreePolicy" : "MultiTree",
    "heuristic" : {
    "heuristicType" : "SCORE_PLUS",
    "class" : "players.heuristics.CoarseTunableHeuristic"
  },
  "K" : 1.0,
  "exploreEpsilon" : 0.3,
  "maxTreeDepth" : 3,
  "treePolicy" : "UCB_Tuned",
  "reuseTree" : True,
  "information" : "Open_Loop",
  "class" : "players.mcts.MCTSParams",
  "budget" : 128
    }

# Mid Dominion Player

dominion_good = {
    "budgetType" : "BUDGET_TIME",
    "rolloutLengthPerPlayer" : True,
    "rolloutTermination" : "END_TURN", 
    "rolloutLength" : 300,
    "opponentTreePolicy" : "MultiTree",
    "heuristic" : {
    "heuristicType" : "SCORE_PLUS",
    "class" : "players.heuristics.CoarseTunableHeuristic"
  },
  "K" : 1.0,
  "exploreEpsilon" : 0.3,
  "maxTreeDepth" : 3,
  "treePolicy" : "UCB_Tuned",
  "reuseTree" : True,
  "information" : "Open_Loop",
  "class" : "players.mcts.MCTSParams",
  "budget" : 64
}

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
dominion_cards = [
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
]
    
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
    args = parser.parse_args()
    
    game = args.game
    folder = args.folder
    
    # Game specific configuration
    match game:
        case "Dominion":
            populate_dominion_params()
            listener = dominion_listener
            good_player = dominion_good
            elite_player = dominion_elite
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
    config["listener"] = folder + "/listener.json"
    config["destDir"] = folder + "/output"
    config["gameParams"] = folder +"/gameParams.json"
    
    # Write configuration files to json
    with open(folder + "/config.json", "w") as f:
        json.dump(config, f)
    with open(folder + "/listener.json", "w") as f:
        json.dump(listener, f)
    with open(folder + "/gameParams.json", "w") as f:
        json.dump(params, f)
        
    # Create player configuration files
    with open(folder + "/players/elite_player.json", "w") as f:
        json.dump(elite_player, f)
    with open(folder + "/players/good_player.json", "w") as f:
        json.dump(good_player, f)
    with open(folder + "/players/osla_player.json", "w") as f:
        json.dump(osla_player, f)
    with open(folder + "/players/random_player.json", "w") as f:
        json.dump(random_player, f)