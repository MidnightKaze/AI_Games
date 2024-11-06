import random
import time

def slow_print(text, delay=1):
    """Function to print text with a slow print effect for immersion."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay / 50)
    print()

def make_choice(choices):
    """Helper function to display choices and get the player's selection."""
    for idx, choice in enumerate(choices):
        print(f"{idx + 1}. {choice}")
    while True:
        try:
            choice = int(input("Choose an option: ")) - 1
            if 0 <= choice < len(choices):
                return choice
            else:
                print("Invalid choice, try again.")
        except ValueError:
            print("Invalid input, please enter a number.")

# --- CHARACTER CLASS ---
class Character:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.health = 100
        self.mana = 50
        self.inventory = []
        self.is_alive = True  # Direct boolean property
        self.completed_quests = []
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.is_alive = False
            slow_print(f"{self.name} has been defeated!")
    
    def heal(self, amount):
        self.health += amount
        slow_print(f"{self.name} heals for {amount} HP!")

    def attack(self, enemy):
        damage = random.randint(10, 30)
        slow_print(f"{self.name} attacks {enemy.name} for {damage} damage!")
        enemy.take_damage(damage)

    def apply_item(self, item):
        self.inventory.append(item)
        slow_print(f"{self.name} receives a new item: {item}")
    
    def view_inventory(self):
        slow_print(f"{self.name}'s Inventory: {', '.join(self.inventory)}")

# --- ENEMY CLASS ---
class Enemy:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack
        self.is_alive = True  # Direct boolean property

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.is_alive = False
            slow_print(f"{self.name} has been defeated!")
    
    def attack(self, character):
        damage = random.randint(self.attack // 2, self.attack)
        slow_print(f"{self.name} attacks {character.name} for {damage} damage!")
        character.take_damage(damage)

# --- STORY STAGES ---
def stage_1(character):
    slow_print(f"\nWelcome to the Village of Kageyama, {character.name}.")
    slow_print("A mysterious Seer approaches you and offers an ancient scroll...")

    choices = ["Follow the Seer's Guidance", "Seek the Elder's Wisdom", "Check Inventory"]
    choice = make_choice(choices)
    
    if choice == 0:
        slow_print("You decide to follow the Seer's guidance into the Sacred Forest.")
        character.completed_quests.append("Seer's Guidance")
        forest_encounter(character)
    elif choice == 1:
        slow_print("You decide to seek Master Hiroshi's wisdom.")
        slow_print("Master Hiroshi tells you to trust your instincts, and gives you a sword technique.")
        character.apply_item("Fireproof Charm")
        character.completed_quests.append("Elder's Wisdom")
        forest_encounter(character)
    elif choice == 2:
        character.view_inventory()
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
        character.take_damage(20)

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
        character.completed_quests.append("Trial of Fire")
    elif choice == 1:
        slow_print("You try to bargain with the Kitsune, offering your sword. She accepts and grants you the Phoenix Feather.")
        character.apply_item("Phoenix Feather")
        character.completed_quests.append("Bargained with Kitsune")

def fire_trial(character):
    slow_print("The ground bursts into flames! You must cross the fiery path.")
    success = random.choice([True, False])
    if success:
        slow_print("You bravely cross the flames and survive!")
    else:
        slow_print("You are scorched by the flames, but endure the pain!")
        character.take_damage(20)

def stage_3(character):
    slow_print("\nYou arrive at Tetsu Village, where you must forge the Blade of the Eternal Dragon.")
    slow_print("The blacksmith's apprentice tells you that the steel lies at the top of Mount Tetsu.")
    
    choices = ["Take the trusted path", "Venture alone", "Check Inventory"]
    choice = make_choice(choices)

    if choice == 0:
        slow_print("You take the longer, safer path and reach the top of the mountain.")
        slow_print("A Guardian Dragon challenges you, but you defeat it with courage!")
        character.apply_item("Blade of the Eternal Dragon")
        character.completed_quests.append("Guardian Dragon Defeated")
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
    elif choice == 1:
        slow_print("You sneak into the fortress, avoiding detection and traps.")
        slow_print("You confront Kurayami in his lair!")
        enemy_battle(character)

def enemy_battle(character):
    kurayami = Enemy("Kurayami", 100, 20)
    slow_print(f"Kurayami, the dark sorcerer, stands before you. He is powerful!")
    
    while character.is_alive and kurayami.is_alive:
        slow_print(f"\nYour Health: {character.health} | Kurayami's Health: {kurayami.health}")
        choices = ["Attack", "Defend"]
        choice = make_choice(choices)

        if choice == 0:
            character.attack(kurayami)
        else:
            slow_print("You brace yourself for Kurayami's next attack.")
        
        if kurayami.is_alive:
            kurayami.attack(character)

    if character.is_alive:
        slow_print("You have defeated Kurayami and freed the Phoenix!")
        if "Trial of Fire" in character.completed_quests:
            slow_print("Thanks to your fire resistance, the Phoenix is freed unharmed!")
        else:
            slow_print("The Phoenix is weakened, but free at last!")
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