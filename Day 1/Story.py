"""
This was just copied and pasted from Game.py since that uhh kind of started evolving cuz of ChatGPT :)
"""

import random
import time

def slow_print(text, delay=1):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay / 50)
    print()

def stage_1(character):
    slow_print(f"\nWelcome to the Village of Kageyama, {character.name}.")
    slow_print("A mysterious Seer approaches you and offers an ancient scroll...")
    
    # Add option to check inventory before making a choice
    choices = ["Follow the Seer's Guidance", "Seek the Elder's Wisdom", "Check Inventory"]
    choice = make_choice(choices)
    
    if choice == 0:
        slow_print("You decide to follow the Seer's guidance into the Sacred Forest.")
        forest_encounter(character)
    elif choice == 1:
        slow_print("You decide to seek Master Hiroshi's wisdom.")
        slow_print("Master Hiroshi tells you to trust your instincts, and gives you a sword technique.")
        character.apply_item("Fireproof Charm")
        forest_encounter(character)
    elif choice == 2:
        character.view_inventory()
        # After viewing inventory, ask them again what to do next
        stage_1(character)

def forest_encounter(character):
    slow_print("\nAs you venture deeper into the Sacred Forest, the path becomes unclear...")
    slow_print("You are approached by a mysterious Tengu, the guardian of the Forgotten Shrine.")
    
    choices = ["Answer the Tengu's riddle", "Attempt to fight the Tengu", "Check Inventory"]
    choice = make_choice(choices)

    if choice == 0:
        slow_print("You solve the riddle, and the Tengu allows you to pass, revealing the Phoenix's first feather.")
        character.apply_item("Phoenix Feather")
    else:
        slow_print("You attempt to fight the Tengu, but it overwhelms you with its magic!")
        character.health -= 20
        slow_print(f"Your health is now {character.health}.")

    slow_print("You exit the forest with the Phoenix Feather and prepare to continue your journey.")

def stage_2(character):
    slow_print("\nYou arrive at the Forgotten Shrine, where the first feather of the Jade Phoenix rests.")
    slow_print("A Kitsune, the fox spirit, appears and challenges you to three trials.")
    
    choices = ["Accept the Kitsune's Challenge", "Bargain with the Kitsune", "Check Inventory"]
    choice = make_choice(choices)

    if choice == 0:
        slow_print("You decide to face the trials. First, the Trial of Fire!")
        fire_trial(character)
        slow_print("You pass the Trial of Fire and gain the Kitsune's Blessing!")
        character.apply_item("Fireproof Charm")
    else:
        slow_print("You try to bargain with the Kitsune, offering your sword. She accepts and grants you the Phoenix Feather.")
        character.apply_item("Phoenix Feather")

def fire_trial(character):
    slow_print("The ground bursts into flames! You must cross the fiery path.")
    success = random.choice([True, False])
    if success:
        slow_print("You bravely cross the flames and survive!")
    else:
        slow_print("You are scorched by the flames, but endure the pain!")
        character.health -= 20
        slow_print(f"Your health is now {character.health}.")

def stage_3(character):
    slow_print("\nYou arrive at Tetsu Village, where you must forge the Blade of the Eternal Dragon.")
    slow_print("The blacksmith's apprentice tells you that the steel lies at the top of Mount Tetsu.")
    
    choices = ["Take the trusted path", "Venture alone", "Check Inventory"]
    choice = make_choice(choices)

    if choice == 0:
        slow_print("You take the longer, safer path and reach the top of the mountain.")
        slow_print("A Guardian Dragon challenges you, but you defeat it with courage!")
        character.apply_item("Blade of the Eternal Dragon")
    else:
        slow_print("You venture alone, risking traps and dangers. You barely survive an avalanche!")
        slow_print("However, you still reach the summit and gain the Eternal Steel.")
        character.apply_item("Blade of the Eternal Dragon")

def stage_4(character):
    slow_print("\nYou have the Blade of the Eternal Dragon. It's time to face Kurayami.")
    slow_print("His fortress is looming ahead. You must decide how to approach.")
    
    choices = ["Storm the Fortress", "Infiltrate the Fortress", "Check Inventory"]
    choice = make_choice(choices)

    if choice == 0:
        slow_print("You charge the fortress with the Emperor's army, fighting through waves of enemies!")
        enemy_battle(character)
    else:
        slow_print("You sneak into the fortress, avoiding detection and traps.")
        slow_print("You confront Kurayami in his lair!")
        enemy_battle(character)

def enemy_battle(character):
    kurayami = Enemy("Kurayami", 100, 20)
    slow_print(f"Kurayami, the dark sorcerer, stands before you. He is powerful!")
    
    while character.is_alive() and kurayami.is_alive():
        slow_print(f"\nYour Health: {character.health} | Kurayami's Health: {kurayami.health}")
        choices = ["Attack", "Defend"]
        choice = make_choice(choices)

        if choice == 0:
            character.attack(kurayami)
        else:
            slow_print("You brace yourself for Kurayami's next attack.")
        
        if kurayami.is_alive():
            kurayami.attack(character)

    if character.is_alive():
        slow_print("You have defeated Kurayami and freed the Phoenix!")
    else:
        slow_print("You have been defeated by Kurayami. The Phoenix remains imprisoned...")

def game_over():
    slow_print("The journey ends here. Would you like to play again?")
    play_again = input("Enter 'yes' to play again or 'no' to quit: ").strip().lower()
    if play_again == 'yes':
        main()

def main():
    slow_print("Welcome to 'The Quest for the Jade Phoenix'!")
    name = input("Enter your character's name: ")
    character = Character(name, "Warrior")
    
    stage_1(character)
    stage_2(character)
    stage_3(character)
    stage_4(character)

    if character.is_alive():
        slow_print(f"\nCongratulations {character.name}, you have completed your quest and freed the Jade Phoenix!")
    else:
        game_over()

# Start the game
if __name__ == "__main__":
    main()