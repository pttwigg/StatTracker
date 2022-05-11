import json
from Player import *


# Reads in all players from the playerdata file, lists them, and, prompts the user to choose a player.
# Optional boolean argument to include option to return without choosing a player.
# Returns a player object, or a zero if the user chooses to return.
def get_player_choice(ret=False):
    # Open the file to read
    file = open('playerdata.json')

    # Load the json data into playerdata
    playerdata = json.load(file)

    file.close()

    # Get a list of all possible ids
    id_list = []
    for i in playerdata["players"]:
        id_list.append(i["id"])

    print("\n\n\nChoose a player\n")

    # Get a valid choice from the user
    while True:
        print("{:<5} {:<30} {:<25} {:<10}".format('id#', 'Name', 'Team', 'Catcher'))

        # Print every player in the file
        for i in playerdata["players"]:
            print("{:<5} {:<30} {:<25} {:<10}".format(i["id"],
                                                      i["info"]["firstname"] + ' ' + i["info"]["lastname"],
                                                      i["info"]["team"],
                                                      i["info"]["catcher"]))

        # Show option to enter -1 to return
        if ret:
            print("\n{:<5} {:<30}".format("-1", "Return"))

        # Gets the user's choice
        choice = input("\n\n\nPlease enter the id# of the player: ")

        # Test if user enters a number
        if not choice.isdigit() and int(choice) != -1:
            print("\n\n\nPlease enter a number\n\n\n")
            continue
        # User chooses to return
        elif int(choice) == -1 and ret:
            return 0
        # Test if user enters a valid id
        elif int(choice) not in id_list:
            print("\n\n\nNo player with that id exists\n\n\n")
            continue
        # User has entered a valid number, break entry loop
        else:
            choice = int(choice)    # Convert choice to in
            break

    # Creates a Player object for the chosen player
    player = Player(playerdata["players"][choice])

    # Print the player's name
    print("\n\nChosen player:", player.data["info"]["firstname"], player.data["info"]["lastname"])

    return player


# Write a player to the playerdata file.
def write_to_file(player_to_save):
    # Open the file to read
    file = open('playerdata.json', 'r+')

    # Load the json data into playerdata
    playerdata = json.load(file)

    # Go back to the beginning of the file
    file.seek(0)

    # Player is new (id of -1), give them a new id and write to file
    if player_to_save["id"] == -1:
        id_list = []

        # Get a list of all possible ids
        for i in playerdata["players"]:
            id_list.append(i["id"])

        # Sets the new ID to the first available one
        player_to_save["id"] = id_list[-1] + 1

        # Add the player to the "players" list in the file
        playerdata["players"].append(player_to_save)

        # Go back to the beginning of the file
        file.seek(0)

        # convert back to json.
        json.dump(playerdata, file, indent=4)
        file.close()

    # Not a new player, update their entry in the file
    else:
        # Update the entry in the file
        playerdata["players"][player_to_save["id"]] = player_to_save

        # Go back to the beginning of the file
        file.seek(0)

        # convert back to json.
        json.dump(playerdata, file, indent=4)
        file.close()
