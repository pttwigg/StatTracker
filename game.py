from utils import *


class Game:
    # Initialize the game object
    def __init__(self):
        # Game mode. 0 = End Game, 1 = Offense, 2 = Defense
        self.mode = -1

        # Choose a player object to track for the game
        self.player = get_player_choice()

        # Dictionary that holds the player's stats for the game
        self.game_stats = {
            'G': 1,
            'PA': 0,
            'AB': 0,
            'H': 0,
            'SO': 0,
            'BB': 0,
            'B1': 0,
            'B2': 0,
            'B3': 0,
            'HR': 0,
            'RBI': 0,
            'R': 0,
            'HBP': 0,
            'FC': 0,
            'SB': 0,
            'CS': 0,
            'PO': 0,
            'A': 0,
            'E': 0,
            'DSB': 0,
            'DCS': 0
        }

    # Begin the game
    def start(self):
        # Loop to get starting mode from the user
        while True:
            print("\n\n\nWould you like to start on offense or defense?")
            print("\n1: Offense\n2: Defense")

            # Get the user's choice
            choice = input("\n\n\nEnter choice: ")

            # Test if input is number
            if not choice.isdigit():
                print("\nPlease enter a number")
                continue
            # Test if input is in range
            elif int(choice) != 1 and int(choice) != 2:
                print("\nPlease enter a valid input")
                continue
            # Valid input
            else:
                self.mode = int(choice)     # Change the mode to an integer
                break

        # Loop game until the end game flag is set (0)
        while self.mode != 0:
            # Offense mode
            if self.mode == 1:
                # Enter offense mode and set mode to next mode
                self.mode = self.offense_mode()
            # Defense mode
            elif self.mode == 2:
                # Enter defense mode, and set mode to next mode
                # Pass boolean argument for whether player is a catcher
                self.mode = self.defense_mode(self.player.data["info"]["catcher"])

        # Ask if user wants to keep the stats from the game or discard them
        save = input("\nWould you like to add the player's stats from this game to their totals? [Y/n]: ")

        # User enters yes, save stats
        if save == 'y' or save == 'Y':
            self.player.add_stats(self.game_stats)
            self.player.save()
        # Skip saving stats
        else:
            print("Stats discarded")

        return

    # Tracks stats for offense. Starts in At-Bat Mode, then switches to either On-Base Mode or Defense Mode
    # depending on the outcome of the at-bat.
    # Returns 0 to end game, 2 to go to Defense mode
    def offense_mode(self):
        # Get valid outcome from user
        while True:
            print("\n\n\nAt-Bat Mode\n")
            print("{:<20} {:<20} {:<20} {:<20}".format('1: Single', '2: Double', '3: Triple', '4: Home Run'))
            print("{:<20} {:<20} {:<20} {:<20}".format('5: Strikeout', '6: Walk', '7: Groundout', '8: Lineout'))
            print("{:<20} {:<20} {:<20} {:<20}".format('9: Flyout', '10: FC', '11: ROE', '12: HBP'))
            print("13: Switch to On Base")
            print("0: End Game")

            # Get the user's choice
            res = input("\n\n\nEnter choice: ")

            # Test if input is number
            if not res.isdigit():
                print("\nPlease enter a number")
                continue
            # Test if input is in range
            elif int(res) < 0 or int(res) > 13:
                print("\nPlease enter a valid input")
                continue
            # Valid input
            else:
                res = int(res)  # Convert to an integer
                break

        ##### At-bat Outcomes #####
        # Single
        if res == 1:
            self.game_stats["RBI"] += self._rbi_prompt()    # Get number of RBI's
            self.game_stats["PA"] += 1
            self.game_stats["AB"] += 1
            self.game_stats["H"] += 1
            self.game_stats["B1"] += 1
            return self.onbase_mode()       # Switch to On-base mode and return the flag it sets
        # Double
        elif res == 2:
            self.game_stats["RBI"] += self._rbi_prompt()    # Get number of RBI's
            self.game_stats["PA"] += 1
            self.game_stats["AB"] += 1
            self.game_stats["H"] += 1
            self.game_stats["B2"] += 1
            return self.onbase_mode()       # Switch to On-base mode and return the flag it sets
        # Triple
        elif res == 3:
            self.game_stats["RBI"] += self._rbi_prompt()    # Get number of RBI's
            self.game_stats["PA"] += 1
            self.game_stats["AB"] += 1
            self.game_stats["H"] += 1
            self.game_stats["B3"] += 1
            return self.onbase_mode()       # Switch to On-base mode and return the flag it sets
        # Home Run
        elif res == 4:
            self.game_stats["RBI"] += self._rbi_prompt(1,4)  # Get number of RBI's
            self.game_stats["PA"] += 1
            self.game_stats["AB"] += 1
            self.game_stats["H"] += 1
            self.game_stats["HR"] += 1
            self.game_stats["R"] += 1
            return 2        # Switch to Defense mode
        # Strikeout
        elif res == 5:
            self.game_stats["PA"] += 1
            self.game_stats["AB"] += 1
            self.game_stats["SO"] += 1
            return 2        # Switch to Defense mode
        # Walk
        elif res == 6:
            self.game_stats["RBI"] += self._rbi_prompt(0,1)  # Get number of RBI's
            self.game_stats["PA"] += 1
            self.game_stats["BB"] += 1
            return self.onbase_mode()       # Switch to On-base mode and return the flag it sets
        # Groundout
        elif res == 7:
            print("Reminder: No RBI's should be given when grounding into double play...")
            rbis = self._rbi_prompt()       # Get number of RBI's
            self.game_stats["RBI"] += rbis
            self.game_stats["PA"] += 1

            # Count an AB if there is no sacrifice
            if not rbis:
                self.game_stats["AB"] += 1

            return 2        # Switch to Defense mode
        # Lineout/Flyout (both accumulate same stats)
        elif res == 8 or res == 9:
            rbis = self._rbi_prompt()       # Get number of RBI's
            self.game_stats["RBI"] += rbis
            self.game_stats["PA"] += 1

            # Count an AB if there is no sacrifice
            if not rbis:
                self.game_stats["AB"] += 1

            return 2        # Switch to Defense mode
        # Fielder's Choice
        elif res == 10:
            self.game_stats["RBI"] += self._rbi_prompt(0,2)  # Get number of RBI's
            self.game_stats["AB"] += 1
            self.game_stats["PA"] += 1
            self.game_stats["FC"] += 1
            return self.onbase_mode()       # Switch to On-base mode and return the flag it sets
        # Reach on Error
        elif res == 11:
            print("(Only count RBI if runner would have scored regardless of error)")
            self.game_stats["RBI"] += self._rbi_prompt()    # Get number of RBI's
            self.game_stats["PA"] += 1
            return self.onbase_mode()       # Switch to On-base mode and return the flag it sets
        # Hit by Pitch
        elif res == 12:
            self.game_stats["RBI"] += self._rbi_prompt(0,1)  # Get number of RBI's
            self.game_stats["PA"] += 1
            self.game_stats["HBP"] += 1
            return self.onbase_mode()       # Switch to On-base mode and return the flag it sets
        # Switch to On-base mode (Useful if user starts inning on base)
        elif res == 13:
            return self.onbase_mode()       # Switch to On-base mode and return the flag it sets
        # End Game
        elif res == 0:
            # Get user's choice
            end_game = input("Are you sure you want to end the game? [y/N]: ")

            # User chooses yes, return flag to end game
            if end_game == 'y' or end_game == 'Y':
                return 0    # Return end game flag
            # User does not select yes, return flag for offense mode
            else:
                return 1    # Stay in Offense Mode

    # Gets and returns the number of rbis the player got on the play, with bounds for allowed number or RBI's
    def _rbi_prompt(self, min=0, max=3):
        # Get a valid number of RBI's from the user
        while True:
            # Get number of RBI's from the user
            rbis = input("\nEnter the number of RBI's the player got: ")

            # Test if input is number
            if not rbis.isdigit():
                print("\nPlease enter a number")
                continue
            # Test if input is in range
            elif int(rbis) < min or int(rbis) > max:
                print("\nPlease enter a valid number of RBIs")
                continue
            # Valid input
            else:
                return int(rbis)

    # Collects stats for when the player is on base. Returns 0, 1, or 2 to indicate the next game mode
    def onbase_mode(self):
        # Stay in mode until return
        while True:
            invalid = True  # Denotes validity of input

            # Get valid outcome from user
            while invalid:
                print("\n\n\nOn-Base Mode\n")
                print("1: Steal Attempt")
                print("2: Score")
                print("3: Switch to Defense Mode")
                print("4: Switch to Offense Mode")
                print("0: End Game")

                # Get the user's choice
                res = input("\n\n\nEnter choice: ")

                # Test if input is number
                if not res.isdigit():
                    print("\nPlease enter a number")
                    continue
                # Test if input is in range
                elif int(res) < 0 or int(res) > 4:
                    print("\nPlease enter a valid input")
                    continue
                # Valid input
                else:
                    res = int(res)
                    invalid = False     # Leave the input loop

            ##### Baserunning Outcomes #####
            # Steal attempt
            if res == 1:
                # Get outcome of steal attempt from user
                while True:
                    print("\n\n\nSteal Attempt\n")
                    print("{:<20} {:<20} {:<20}".format('1: Success', '2: Caught', '3: FI/Cancel'))

                    # Get the user's choice
                    att = input("\n\n\nEnter Choice")

                    # Test if input is number
                    if not att.isdigit():
                        print("\nPlease enter a number")
                        continue
                    # Safe
                    elif int(att) == 1:
                        self.game_stats["SB"] += 1
                        break
                    # Out
                    elif int(att) == 2:
                        self.game_stats["CS"] += 1
                        return 2        # Switch to Defense mode
                    # No throw / cancel
                    elif int(att) == 3:
                        break
                    # Input out of range
                    else:
                        print("\nPlease enter a valid input")
                        continue
            # Score
            elif res == 2:
                self.game_stats["R"] += 1
                return 2        # Return Defense Mode flag
            # Go to Defense mode
            elif res == 3:
                return 2        # Return Defense Mode flag
            # Go to Offense mode
            elif res == 4:
                return 1        # Return Offense Mode flag
            # End game
            elif res == 0:
                return 0        # Return end game flag

    # Collects stats for when the player is on defense. Inputs a boolean argument denoting whether the player is a
    # catcher to know whether to show catching options. Returns 0, 1, or 2 denoting next mode to go to.
    def defense_mode(self, catcher):
        # Get outcome from user
        while True:
            print("\n\n\nDefense Mode\n")
            print("{:<20} {:<20} {:<20}".format('1: Putout', '2: Assist', '3: Error'))
            # Show catcher options if the player is a catcher
            if catcher:
                print("4: Steal Attempt")
            print("5: Switch to Offense Mode")
            print("0: End Game")

            # Get the outcome from the user
            res = input("\n\n\nEnter choice: ")

            # Test if input is number
            if not res.isdigit():
                print("\nPlease enter a number")
                continue
            # Test if input is in range
            elif int(res) < 0 or int(res) > 5:
                print("\nPlease enter a valid input")
                continue
            # Give an error if the user chooses a catcher option for a player who is not a catcher
            elif int(res) == 4 and not catcher:
                print("\nPlease enter a valid input")
            # Valid input
            else:
                res = int(res)
                break

        ##### Defensive play outcomes #####
        # Putout
        if res == 1:
            self.game_stats["PO"] += 1
        # Assist
        elif res == 2:
            self.game_stats["A"] += 1
        # Error
        elif res == 3:
            self.game_stats["E"] += 1
        # Steal attempt
        elif res == 4:
            # Get a valid outcome for the steal attempt
            while True:
                print("\n\n\nSteal Attempt\n")
                print("{:<20} {:<20} {:<20}".format('1: Steal', '2: Caught', '3: FI/Cancel'))

                # Get the user's choice
                att = input("\n\n\nEnter Choice: ")

                # Test if input is number
                if not att.isdigit():
                    print("\nPlease enter a number")
                    continue
                # Safe
                elif int(att) == 1:
                    self.game_stats["DSB"] += 1
                    break
                # Out
                elif int(att) == 2:
                    self.game_stats["DCS"] += 1
                    break
                # No throw / cancel
                elif int(att) == 3:
                    break
                # Input out of range
                else:
                    print("\nPlease enter a valid input")
                    continue
        # Go to Offense mode
        elif res == 5:
            return 1    # Set Offense Mode flag
        # End game
        elif res == 0:
            return 0    # Set end game flag

        return 2    # Loop back to Defense Mode
