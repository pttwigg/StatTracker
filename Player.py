import utils


class Player:
    # Initialize the player. If no dictionary with player info is passed in, initialize all info as blank,
    # otherwise used info that is passed in
    def __init__(self, info=0):
        # If no value is passed in during player creation, create blank player
        if info == 0:
            # Set all attributes to be blank
            self.data = {
                "id": -1,
                "info":
                    {
                        "firstname": "",
                        "lastname": "",
                        "team": "",
                        "number": 0,
                        "catcher": False
                    },
                "stats":
                    {
                        "G": 0,
                        "PA": 0,
                        "AB": 0,
                        "H": 0,
                        "SO": 0,
                        "BB": 0,
                        "B1": 0,
                        "B2": 0,
                        "B3": 0,
                        "HR": 0,
                        "RBI": 0,
                        "R": 0,
                        "HBP": 0,
                        "FC": 0,
                        "SB": 0,
                        "CS": 0,
                        "PO": 0,
                        "A": 0,
                        "E": 0,
                        "DSB": 0,
                        "DCS": 0
                    }
            }
        # If player data is passed in, use it instead
        else:
            self.data = info

    # Add all stats from new_stats to the player's existing stats
    def add_stats(self, new_stats):
        # Loop through stats and add them together
        for key in self.data["stats"]:
            self.data["stats"][key] += new_stats[key]

        print("\nStats added to player")

    # Save the player object to the file
    def save(self):
        utils.write_to_file(self.data)

    # Get the player's info from the user
    def set_info(self):
        print("\nSet user info:")
        firstname = input("Enter the player's first name: ")
        lastname = input("Enter the player's last name: ")
        team = input("Enter the player's team name: ")

        # Test for valid input for number
        while True:
            number = input("Enter the player's number: ")
            # Number is not a digit
            if not number.isdigit():
                print("\nPlease enter a number\n\n\n")
            # Number is a digit, change to int type to save
            else:
                number = int(number)
                break

        # User chooses whether the player is a catcher
        catcher = input("Is the player a catcher?"
                        "(this will affect which options appear when the player is on defense)[y/N]: ")

        # Switch to a boolean value based on the input
        # Player entered yse, set to True
        if catcher == 'y' or catcher == 'Y':
            catcher = True
        # Player did not enter yes, default to False
        else:
            catcher = False

        self.data["info"]["firstname"] = firstname
        self.data["info"]["lastname"] = lastname
        self.data["info"]["team"] = team
        self.data["info"]["number"] = number
        self.data["info"]["catcher"] = catcher
