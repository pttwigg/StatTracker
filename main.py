from game import *
from players_menu import *


# Main menu
def main():
    print("\nWelcome to StatTracker")

    # Loop the main menu until the user chooses to quit
    while True:
        print("\n\n\nMain Menu\n")
        print("1: Start New Game\n2: Players\n3: Quit")

        # Get the user's choice
        user_choice = input("\n\n\nEnter choice: ")

        # Start new game
        if user_choice == '1':
            game = Game()   # Initialize a game object
            game.start()    # Start the game
        # Players Menu
        elif user_choice == '2':
            players_menu()  # Go to the players menu
        # Quit
        elif user_choice == '3':
            return
        # Invalid entry
        else:
            print("\n Please enter a valid number\n\n\n")

# Run the main program
if __name__=="__main__":
    main()