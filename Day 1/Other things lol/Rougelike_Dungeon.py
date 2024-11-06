import random
import time

# Define a function to print text slowly
def slow_print(text, delay=0.05):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

# Define Storyline State
story_state = {
    "rescued_villager": False,
    "artifact_found": False,
    "final_choice": None,
}

# Character, Race, and Class Definitions
class Character:
    def __init__(self, name, char_race, char_class):
        self.name = name
        self.race = char_race
        self.char_class = char_class
        self.health = 100 + char_race.health_bonus + char_class.health_bonus
        self.attack = 10 + char_class.attack_bonus
        self.defense = 5 + char_race.defense_bonus
        self.inventory = []
        self.special_attack_cooldown = 0

    def take_damage(self, damage):
        self.health -= max(damage - self.defense, 0)
        if self.health < 0:
            self.health = 0  # Prevent health from going below zero

    def heal(self, amount):
        self.health = min(self.health + amount, 100)

    def can_use_special_attack(self):
        return self.special_attack_cooldown == 0

    def reset_special_attack(self):
        self.special_attack_cooldown = 3  # Cooldown of 3 turns for Special Attack

    def decrease_cooldown(self):
        if self.special_attack_cooldown > 0:
            self.special_attack_cooldown -= 1

    def use_item(self, item):
        if item == "Healing Potion":
            self.heal(30)
            self.inventory.remove(item)
            slow_print(f"\n{self.name} used a Healing Potion. Health is now {self.health}!")
        else:
            slow_print(f"\n{item} cannot be used.")

class Race:
    def __init__(self, name, health_bonus, defense_bonus):
        self.name = name
        self.health_bonus = health_bonus
        self.defense_bonus = defense_bonus

class Class:
    def __init__(self, name, attack_bonus, health_bonus):
        self.name = name
        self.attack_bonus = attack_bonus
        self.health_bonus = health_bonus

# Race and Class Options
def create_character():
    slow_print("\nWelcome to Character Creation!")
    
    # Choose Race
    races = {
        1: Race("Human", health_bonus=10, defense_bonus=2),
        2: Race("Elf", health_bonus=5, defense_bonus=5),
        3: Race("Dwarf", health_bonus=15, defense_bonus=3)
    }
    slow_print("Choose your race:")
    for key, race in races.items():
        slow_print(f"{key}. {race.name} (Health Bonus: {race.health_bonus}, Defense Bonus: {race.defense_bonus})")
    race_choice = int(input("Enter the number of your chosen race: "))
    chosen_race = races.get(race_choice)

    # Choose Class
    classes = {
        1: Class("Warrior", attack_bonus=5, health_bonus=20),
        2: Class("Mage", attack_bonus=8, health_bonus=5),
        3: Class("Rogue", attack_bonus=7, health_bonus=10)
    }
    slow_print("\nChoose your class:")
    for key, char_class in classes.items():
        slow_print(f"{key}. {char_class.name} (Attack Bonus: {char_class.attack_bonus}, Health Bonus: {char_class.health_bonus})")
    class_choice = int(input("Enter the number of your chosen class: "))
    chosen_class = classes.get(class_choice)

    # Name the Character
    name = input("\nEnter your character's name: ")
    return Character(name, chosen_race, chosen_class)

# Inventory Management
def add_to_inventory(item):
    player.inventory.append(item)
    slow_print(f"{item} has been added to your inventory.")

def display_inventory():
    if player.inventory:
        slow_print("\nInventory:")
        for idx, item in enumerate(player.inventory, 1):
            slow_print(f"{idx}. {item}")
    else:
        slow_print("\nYour inventory is empty.")

# Random Events for Item Acquisition
def random_event():
    events = [
        "You found a Healing Potion lying on the ground.",
        "You stumble upon a treasure chest and find a Magic Stone!",
        "A merchant gives you a Health Elixir as a token of goodwill.",
    ]
    event = random.choice(events)
    slow_print(f"\nRandom Event: {event}")

    # Adding items to inventory
    if "Healing Potion" in event:
        add_to_inventory("Healing Potion")
    elif "Magic Stone" in event:
        add_to_inventory("Magic Stone")
    elif "Health Elixir" in event:
        add_to_inventory("Health Elixir")

# Story Events and Choices
def forest_event():
    slow_print("\nAs you enter the Haunted Forest, an eerie mist surrounds you.")
    slow_print("You hear a faint voice calling for help. Do you investigate?")
    choice = input("1. Investigate the voice\n2. Ignore and move on\nChoose: ")
    
    if choice == "1":
        slow_print("\nYou follow the voice and find a frightened villager.")
        slow_print("The villager thanks you and hands you a Healing Potion.")
        add_to_inventory("Healing Potion")
        story_state["rescued_villager"] = True
    else:
        slow_print("\nYou decide not to take any risks and continue your journey.")

def village_event():
    slow_print("\nYou arrive at a cursed village where people are hiding indoors.")
    slow_print("A village elder approaches you and warns of a dark artifact causing chaos.")
    slow_print("He asks if you will retrieve it to lift the curse.")
    choice = input("1. Accept the quest\n2. Refuse and continue your journey\nChoose: ")

    if choice == "1":
        slow_print("\nThe elder blesses you, granting a temporary health boost.")
        player.heal(20)
        story_state["artifact_found"] = False  # Quest accepted, but artifact not yet found
    else:
        slow_print("\nYou decide the quest is too dangerous and press on without further aid.")

def dungeon_event():
    slow_print("\nYou reach the entrance of an ancient dungeon. Inside, you sense immense power.")
    if story_state["artifact_found"]:
        slow_print("With the artifact in hand, you now have a choice to make...")
        choice = input("1. Destroy the artifact to lift the curse\n2. Keep it for yourself, gaining its power\nChoose: ")

        if choice == "1":
            slow_print("\nYou destroy the artifact, lifting the curse and restoring peace.")
            story_state["final_choice"] = "destroyed"
        else:
            slow_print("\nYou keep the artifact, feeling its dark power coursing through you.")
            player.attack += 5  # Gain a power boost
            story_state["final_choice"] = "kept"
    else:
        slow_print("\nWithout the artifact, you realize you cannot complete the quest.")
        slow_print("Disappointed, you exit the dungeon, unsure of what could have been...")

# Basic Combat System with Attack, Special Attack, Run, and Defend options
class Enemy:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0  # Prevent health from going below zero

def combat(player, enemy):
    slow_print(f"\nCombat started: {player.name} vs {enemy.name}")
    while player.health > 0 and enemy.health > 0:
        slow_print(f"\n{player.name}'s Health: {player.health}, {enemy.name}'s Health: {enemy.health}")
        slow_print("Choose your action:\n1. Attack\n2. Special Attack\n3. Run\n4. Defend\n5. Use Item")
        
        action = input("Enter the number of your action: ")

        if action == "1":  # Regular Attack
            slow_print(f"{player.name} attacks {enemy.name}!")
            enemy.take_damage(player.attack)
            slow_print(f"{enemy.name}'s health is now {enemy.health}")
            if enemy.health <= 0:
                slow_print(f"{enemy.name} is defeated!")
                break

        elif action == "2":  # Special Attack
            if player.can_use_special_attack():
                special_damage = player.attack * 2  # Double damage for special attack
                slow_print(f"{player.name} uses a Special Attack on {enemy.name}!")
                enemy.take_damage(special_damage)
                slow_print(f"{enemy.name} takes {special_damage} damage! Health is now {enemy.health}")
                player.reset_special_attack()
                if enemy.health <= 0:
                    slow_print(f"{enemy.name} is defeated!")
                    break
            else:
                slow_print("Special Attack is on cooldown! Choose another action.")

        elif action == "3":  # Run
            if random.choice([True, False]):  # 50% chance to successfully run
                slow_print(f"{player.name} successfully ran away!")
                return  # Ends the combat
            else:
                slow_print(f"{player.name} tried to run but failed!")

        elif action == "4":  # Defend
            slow_print(f"{player.name} defends, reducing incoming damage!")
            player.defense += 5  # Temporary defense boost for this turn only

        elif action == "5":  # Use Item
            display_inventory()
            if player.inventory:
                item_choice = int(input("\nEnter the number of the item you want to use: "))
                item = player.inventory[item_choice - 1]
                player.use_item(item)
            else:
                slow_print("You don't have any items in your inventory.")

        # Enemy's turn to attack
        if enemy.health > 0:  # Ensure the enemy only attacks if still alive
            slow_print(f"{enemy.name} attacks {player.name} with {enemy.attack} attack power!")
            player.take_damage(enemy.attack)
            slow_print(f"{player.name}'s health is now {player.health}")
        
        # Remove temporary defense boost if the player defended
        if action == "4":
            player.defense -= 5
        
        # Reduce Special Attack cooldown by 1 each turn
        player.decrease_cooldown()

        # Check if player health drops to 0 or below
        if player.health <= 0:
            slow_print(f"{player.name} has been defeated!")
            break

# Enemy Variety
goblin = Enemy("Goblin", health=30, attack=5)
orc = Enemy("Orc", health=50, attack=10)
dark_spirit = Enemy("Dark Spirit", health=80, attack=15)

# Main Game Loop
def main():
    global player
    player = create_character()

    slow_print(f"\nWelcome, {player.name} the {player.race.name} {player.char_class.name}!")
    slow_print("Prepare for your journey...\n")

    # Forest Area
    slow_print("\nYou venture into the Haunted Forest...")
    forest_event()
    random_event()  # Random event here
    combat(player, goblin)
    
    if player.health > 0:
        # Village Area
        slow_print("\nYou proceed to the cursed village...")
        village_event()
        random_event()  # Random event here
        combat(player, orc)
        
    if player.health > 0:
        # Dungeon Area
        slow_print("\nYou arrive at the ancient dungeon...")
        dungeon_event()
        random_event()  # Random event here
        combat(player, dark_spirit)

    # Ending
    if player.health > 0:
        if story_state["final_choice"] == "destroyed":
            slow_print("\nCongratulations! You've lifted the curse and saved the land.")
        elif story_state["final_choice"] == "kept":
            slow_print("\nWith the artifact's power, you become a dark legend feared by all.")
        else:
            slow_print("\nYou've survived, but without completing your quest.")
    else:
        slow_print("\nGame Over! The dungeon claims another soul...")

if __name__ == "__main__":
    main()
