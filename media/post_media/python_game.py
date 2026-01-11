def start_game():
    """Starts the game and presents the introduction."""
    print("Welcome to the Adventure Game!")
    print("You find yourself in a mysterious forest...")
    introduction()

def introduction():
    """Introduces the player to the first choices."""
    print("\nYou see a path diverging into two directions.")
    choice_1()

def choice_1():
    """Presents the first set of choices to the player."""
    print("\nDo you want to:")
    print("1. Explore the cave")
    print("2. Follow the river")
    
    choice = input("Enter 1 or 2: ")
    if choice == "1":
        cave_outcome()
    elif choice == "2":
        river_outcome()
    else:
        print("Invalid choice. Try again.")
        choice_1()

def cave_outcome():
    """Handles the outcome of choosing to explore the cave."""
    print("\nYou enter the cave and hear a low growl.")
    print("Do you want to:")
    print("1. Investigate the sound")
    print("2. Leave the cave")
    
    choice = input("Enter 1 or 2: ")
    if choice == "1":
        dragon_encounter()
    elif choice == "2":
        print("You safely exit the cave but miss out on an adventure.")
        end_game()
    else:
        print("Invalid choice. Try again.")
        cave_outcome()

def dragon_encounter():
    """Handles the encounter with the dragon in the cave."""
    print("\nA dragon appears! It looks hungry.")
    print("Do you want to:")
    print("1. Fight the dragon")
    print("2. Offer it some food")
    
    choice = input("Enter 1 or 2: ")
    if choice == "1":
        print("You bravely fight the dragon and win! You find treasure.")
        end_game("You are rich now!")
    elif choice == "2":
        print("The dragon appreciates your kindness and shares its treasure.")
        end_game("You gained a friend and treasure!")
    else:
        print("Invalid choice. Try again.")
        dragon_encounter()

def river_outcome():
    """Handles the outcome of choosing to follow the river."""
    print("\nYou follow the river and meet a friendly villager.")
    print("Do you want to:")
    print("1. Ask for help")
    print("2. Continue along the river")
    
    choice = input("Enter 1 or 2: ")
    if choice == "1":
        villager_help()
    elif choice == "2":
        print("You get lost in the wilderness.")
        end_game("You wander for days before finding your way home.")
    else:
        print("Invalid choice. Try again.")
        river_outcome()

def villager_help():
    """Handles the interaction with the villager."""
    print("\nThe villager agrees to help you.")
    print("Do you want to:")
    print("1. Go to their village")
    print("2. Decline and continue on your own")
    
    choice = input("Enter 1 or 2: ")
    if choice == "1":
        print("You have a great time in the village, enjoying food and stories.")
        end_game("You've made lifelong friends!")
    elif choice == "2":
        print("You venture back into the forest alone.")
        end_game("Sometimes it's better to have friends.")
    else:
        print("Invalid choice. Try again.")
        villager_help()

def end_game(outcome="Thanks for playing!"):
    """Ends the game and displays the outcome."""
    print(f"\n{outcome}")
    print("Would you like to play again? (yes/no)")
    replay = input().lower()
    if replay == 'yes':
        start_game()
    else:
        print("Goodbye!")

# Start the game
if __name__ == "__main__":
    start_game()