import random
import time

# Helper function to pause and display text slowly for dramatic effect
def slow_print(text, delay=1):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay / 50)
    print()

# Helper function to handle player choices
def make_choice(options):
    while True:
        print("\n".join([f"{i}. {opt}" for i, opt in enumerate(options, 1)]))
        try:
            choice = int(input("Choose an option: ")) - 1
            if 0 <= choice < len(options):
                return choice
            else:
                print("Invalid choice, please choose a valid option.")
        except ValueError:
            print("Invalid choice, please enter a number.")

# Character class to hold the player stats
class Character:
    def __init__(self, name, char_class):
        self.name = name
        self.char_class = char_class
        self.health = 100
        self.items = []  # Inventory to store items
        self.weapon = "Basic Sword"

        # Set character stats based on the chosen class
        if char_class == "Warrior":
            self.strength = random.randint(15, 20)
            self.dexterity = random.randint(5, 10)
            self.intelligence = random.randint(5, 10)
            self.charisma = random.randint(5, 10)
        elif char_class == "Mage":
            self.strength = random.randint(5, 10)
            self.dexterity = random.randint(5, 10)
            self.intelligence = random.randint(15, 20)
            self.charisma = random.randint(10, 15)
        elif char_class == "Archer":
            self.strength = random.randint(10, 15)
            self.dexterity = random.randint(15, 20)
            self.intelligence = random.randint(5, 10)
            self.charisma = random.randint(10, 15)
        elif char_class == "Rogue":
            self.strength = random.randint(10, 15)
            self.dexterity = random.randint(15, 20)
            self.intelligence = random.randint(10, 15)
            self.charisma = random.randint(10, 15)
        elif char_class == "Cleric":
            self.strength = random.randint(5, 10)
            self.dexterity = random.randint(10, 15)
            self.intelligence = random.randint(10, 15)
            self.charisma = random.randint(15, 20)

    def apply_item(self, item):
        """Use or apply an item to modify the character's stats or inventory."""
        if item == "Phoenix Feather":
            self.strength += 5
            self.items.append(item)
            slow_print(f"You feel a surge of power from the Phoenix Feather! +5 Strength!")
        elif item == "Fireproof Charm":
            self.items.append(item)
            slow_print("You have gained the Fireproof Charm. It grants protection from fire-based attacks.")
        elif item == "Blade of the Eternal Dragon":
            self.weapon = "Blade of the Eternal Dragon"
            self.strength += 10
            slow_print(f"You have obtained the Blade of the Eternal Dragon! +10 Strength!")
        elif item == "Healing Potion":
            self.health += 20
            self.items.remove(item)
            slow_print(f"You drink the Healing Potion and recover 20 health! Current health: {self.health}")
        else:
            self.items.append(item)
            slow_print(f"You have acquired a new item: {item}")

    def discard_item(self, item):
        """Allow the player to discard an item from their inventory."""
        if item in self.items:
            self.items.remove(item)
            slow_print(f"You have discarded the {item}.")
        else:
            slow_print(f"You don't have the {item} in your inventory to discard.")

    def view_inventory(self):
        """Display the player's current inventory."""
        if not self.items:
            slow_print("Your inventory is empty.")
        else:
            slow_print("Your current inventory contains:")
            for item in self.items:
                print(f"- {item}")

    def attack(self, enemy):
        if self.weapon == "Blade of the Eternal Dragon":
            damage = random.randint(15, 25)
        else:
            damage = random.randint(5, 15)
        enemy.health -= damage
        slow_print(f"You attack {enemy.name} for {damage} damage!")

    def is_alive(self):
        return self.health > 0

# Enemy class to represent enemies in the game
class Enemy:
    def __init__(self, name, health, strength):
        self.name = name
        self.health = health
        self.strength = strength

    def attack(self, player):
        """Attack the player."""
        damage = random.randint(5, self.strength)
        slow_print(f"{self.name} attacks {player.name} for {damage} damage!")
        player.health -= damage

    def is_alive(self):
        return self.health > 0

    def increase_difficulty(self, level):
        """Increase the enemy's difficulty based on the game progression."""
        self.health += 10 * level
        self.strength += 5 * level
        slow_print(f"The enemy grows stronger! Health: {self.health}, Strength: {self.strength}")

# Combat Class
class Combat:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

    def player_action(self):
        """Allow the player to choose an action during combat."""
        actions = ["Attack", "Defend", "Use Item", "Flee"]
        choice = make_choice(actions)

        if choice == 0:  # Attack
            return self.player.attack(self.enemy)
        elif choice == 1:  # Defend
            return self.player.defend()
        elif choice == 2:  # Use Item
            if self.player.items:
                item = input(f"Choose an item to use from {self.player.items}: ")
                if item in self.player.items:
                    self.player.apply_item(item)
                    return 0
                else:
                    slow_print(f"You don't have {item} in your inventory.")
                    return self.player_action()
            else:
                slow_print("You have no items to use!")
                return self.player_action()
        elif choice == 3:  # Flee
            slow_print(f"{self.player.name} tries to flee!")
            if random.random() > 0.5:
                slow_print(f"{self.player.name} successfully fled the battle!")
                return "fled"
            else:
                slow_print(f"{self.player.name} failed to flee!")
                return 0

    def enemy_action(self):
        """Allow the enemy to take an action."""
        action = random.choice(["Attack", "Defend"])
        if action == "Attack":
            self.enemy.attack(self.player)
        else:  # Defend
            slow_print(f"{self.enemy.name} defends, reducing incoming damage.")

    def start(self):
        """Start the combat loop."""
        while self.player.is_alive() and self.enemy.is_alive():
            # Player's turn
            damage = self.player_action()

            # If player fled, end combat
            if damage == "fled":
                break

            # Enemy's turn
            self.enemy_action()

            # Display health status
            slow_print(f"\n{self.player.name} Health: {self.player.health}, {self.enemy.name} Health: {self.enemy.health}")

        if self.player.is_alive():
            slow_print(f"{self.player.name} wins the battle!")
        else:
            slow_print(f"{self.player.name} has been defeated...")

# Game stages and story functions

def choose_class():
    slow_print("Choose your character class:")
    classes = ["Warrior", "Mage", "Archer", "Rogue", "Cleric"]
    for i, c in enumerate(classes, 1):
        print(f"{i}. {c}")

    while True:
        try:
            choice = int(input("Enter the number of your class: ")) - 1
            if 0 <= choice < len(classes):
                return classes[choice]
            else:
                print("Invalid choice, please choose a valid class.")
        except ValueError:
            print("Invalid choice, please enter a number.")

def create_character():
    slow_print("Welcome to 'The Quest for the Jade Phoenix'!")
    
    # Prompt the user for their name
    name = input("Enter your character's name: ")
    
    # Prompt the user to choose a class
    char_class = choose_class()
    
    # Create the character object
    character = Character(name, char_class)
    
    # Display the created character's information
    slow_print(f"\n{character.name}, the {char_class}, has been created!")
    slow_print(f"Stats: Strength={character.strength}, Dexterity={character.dexterity}, Intelligence={character.intelligence}, Charisma={character.charisma}")
    
    return character

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