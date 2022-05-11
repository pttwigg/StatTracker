from utils import *
from types import SimpleNamespace


# Players Menu main loop. User can select to view a player's stats, create a new player, or leave the menu.
def players_menu():
    # Stay in the players menu until return
    while True:
        # Boolean denoting validity of input
        invalid = True

        # Get a valid entry
        while invalid:
            print("\n\n\nPlayers Menu\n")
            print("1: View Stats\n2: Create New Player\n3: Return")

            # Get the user's choice
            choice = input("\n\n\nEnter an option: ")

            # Test if input is number
            if choice.isdigit() == False:
                print("\nPlease enter a number")
                continue
            # Test if input is in range
            elif int(choice) > 1 and int(choice) > 3:
                print("\nPlease enter a valid input")
                continue
            # Valid input
            else:
                invalid = False

        # User choose View Stats menu
        if choice == '1':
            view_stats()        # View stats menu
        # User choose to create a player
        elif choice == '2':
            create_player()     # Create Player mode
        # User choose to return to the previous menu
        else:
            return


# View the stats of a player. User will be prompted to select a player from the playerdata file. Player will then be
# read in, all mathematical stats will be calculated from the player's basic stats, and all stats will then be listed
# on the screen.
def view_stats():
    # Get a player object from the user, or a 0 if the user chooses instead to return to the players menu.
    player = get_player_choice(True)

    # User chose to return to main menu
    if not player:
        return

    # Create a namespace for the player stats
    s = SimpleNamespace(**player.data["stats"])

    # Calculate all mathematical stats
    BA = _div(s.H, s.AB)                                                    # Batting Average
    TB = s.H + 2*s.B2 + 3*s.B3 + 4*s.HR                                     # Total Bases
    OBP = _div((s.H + s.BB + s.HBP),(s.AB + s.BB + s.HBP))                  # On-Base Pct.
    SLG = _div(TB,s.AB)                                                     # Slugging Pct.
    OPS = OBP + SLG                                                         # On-Base + Slugging
    ISO = _div((TB - s.H),s.AB)                                             # Isolated Power
    XBH = s.B2 + s.B3 + s.HR                                                # Extra Base Hits
    XBHpct = _div(XBH, s.PA)                                                # Extra Base Hits pct.
    XpHpct = _div(XBH, s.H)                                                 # Extra Base Hits per Hit pct.
    SOpW = _div(s.SO, s.BB)                                                 # Strikouts per Walk
    ABpSO = _div(s.AB, s.SO)                                                # At-Bats per Strikout
    ABpRBI = _div(s.AB, s.RBI)                                              # At-Bats per RBI
    IPpct = _div((s.AB - s.SO - s.HR), s.PA)                                # In-Play pct.
    SOpct = _div(s.SO, s.PA)                                                # Strikout pct.
    BBpct = _div(s.BB, s.PA)                                                # Walk pct.
    SBpct = _div(s.SB, (s.SB + s.CS))                                       # Stolen Base pct.
    RSpct = _div((s.R - s.HR),(s.H + s.HBP + s.BB - s.HR))                  # Run Scored pct.
    RC = _div(((s.H + s.BB - s.CS) * (TB + (.55 * s.SB))),(s.AB + s.BB))    # Runs Created
    CH = s.PO + s.A + s.E                                                   # Defensive Chances
    FLDpct = _div((CH - s.E), CH)                                           # Fielding pct.
    DCSpct = _div(s.DCS, (s.DSB + s.DCS))                                   # Catcher Caught Stealing pct.

    # Print out all stats (round percentages to 3 places)
    print("Batting Stats:")
    print("\tGames Played:      ", s.G)
    print("\tPlate Appearances: ", s.PA)
    print("\tAt-Bats:           ", s.AB)
    print("\tRuns:              ", s.R)
    print("\tHits:              ", s.H)
    print("\tDoubles:           ", s.B2)
    print("\tTriples:           ", s.B3)
    print("\tHome Runs:         ", s.HR)
    print("\tRuns Batted In:    ", s.RBI)
    print("\tAt-Bats per RBI:   ", "%.3f" % round(ABpRBI, 3))
    print("\tStrikeouts:        ", s.SO)
    print("\tStrikeout %:       ", "%.3f" % round(SOpct,3))
    print("\tAB per Strikeout:  ", "%.3f" % round(ABpSO,3))
    print("\tWalks:             ", s.BB)
    print("\tWalk %:            ", "%.3f" % round(BBpct,3))
    print("\tStrikeout per Walk:", "%.3f" % round(SOpW,3))
    print("\tHit By Pitch:      ", s.HBP)
    print("\tFielder's Choice:  ", s.FC)
    print("\tTotal Bases:       ", TB)
    print("\tBatting Average:   ", "%.3f" % round(BA, 3))
    print("\tOn-Base %:         ", "%.3f" % round(OBP,3))
    print("\tSlugging %:        ", "%.3f" % round(SLG,3))
    print("\tOn-Base + Slugging:", "%.3f" % round(OPS,3))
    print("\tIsolated Power:    ", "%.3f" % round(ISO,3))
    print("\tRuns Created:      ", "%.3f" % round(RC,3))
    print("\tIn-Play %:         ", "%.3f" % round(IPpct,3))
    print("\tExtra Base Hits:   ", XBH)
    print("\tExtra Base Hit %:  ", "%.3f" % round(XBHpct,3))
    print("\tXBH per Hit:       ", "%.3f" % round(XpHpct,3))
    print("Baserunning:")
    print("\tRuns Scored %:     ", "%.3f" % round(RSpct,3))
    print("\tStolen Bases:      ", s.SB)
    print("\tCaught Stealing:   ", s.CS)
    print("\tStolen Base %:     ", "%.3f" % round(SBpct,3))
    print("Fielding:")
    print("\tAssists:           ", s.A)
    print("\tPutouts:           ", s.PO)
    print("\tDefensive Chances: ", CH)
    print("\tFielding %:        ", "%.3f" % round(FLDpct,3))

    # Show catcher stats if applicable
    if player.data["info"]["catcher"]:
        print("Catching:")
        print("\tSB Allowed:        ", s.DSB)
        print("\tCaught Stealing:   ", s.DCS)
        print("\tCaught Stealing %: ", "%.3f" % round(DCSpct,3))

    # Hold the screen
    end = input("\n\n\nPress <enter> to continue: ")

    return


# Divide stats, checking for divide by zero errors (in which case returns 0 in float type)
def _div(n,d):
    # Attempt normal division
    try:
        return n/d
    # Divide-by-zero error, so just set to zero
    except ZeroDivisionError:
        return 0.000


# Creates a new player with user-provided info, and adds it to playerdata file
def create_player():
    # Create a new instance of the Player class
    new_player = Player()

    # Get the player's info from the user
    new_player.set_info()

    # Save the new player to the file
    new_player.save()

    return