import random

class Character:
    def __init__(self, name, char_class):
        self.name = name
        self.char_class = char_class
        self.stats = {}
        self.create_character()

    def create_character(self):
        if self.char_class == "Warrior":
            self.stats = {
                'Strength': random.randint(12, 18),
                'Dexterity': random.randint(8, 12),
                'Intelligence': random.randint(6, 10),
                'Constitution': random.randint(12, 16),
                'Charisma': random.randint(6, 12)
            }
        elif self.char_class == "Mage":
            self.stats = {
                'Strength': random.randint(4, 8),
                'Dexterity': random.randint(8, 12),
                'Intelligence': random.randint(16, 20),
                'Constitution': random.randint(6, 10),
                'Charisma': random.randint(10, 14)
            }
        elif self.char_class == "Rogue":
            self.stats = {
                'Strength': random.randint(8, 12),
                'Dexterity': random.randint(14, 18),
                'Intelligence': random.randint(8, 12),
                'Constitution': random.randint(10, 14),
                'Charisma': random.randint(12, 16)
            }
        elif self.char_class == "Cleric":
            self.stats = {
                'Strength': random.randint(8, 12),
                'Dexterity': random.randint(10, 14),
                'Intelligence': random.randint(10, 14),
                'Constitution': random.randint(10, 14),
                'Charisma': random.randint(14, 18)
            }
        elif self.char_class == "Ranger":
            self.stats = {
                'Strength': random.randint(12, 16),
                'Dexterity': random.randint(12, 16),
                'Intelligence': random.randint(8, 12),
                'Constitution': random.randint(12, 16),
                'Charisma': random.randint(6, 10)
            }

    def display_character(self):
        print(f"\nCharacter Name: {self.name}")
        print(f"Character Class: {self.char_class}")
        print("Stats:")
        for stat, value in self.stats.items():
            print(f"{stat}: {value}")

def create_character():
    print("Welcome to the Character Creation System!")
    name = input("Enter your character's name: ")
    
    # Class selection
    print("\nChoose a class:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Rogue")
    print("4. Cleric")
    print("5. Ranger")
    class_choice = int(input("Enter the number of your chosen class: "))
    
    # Map the class choice to a class name
    class_mapping = {
        1: "Warrior",
        2: "Mage",
        3: "Rogue",
        4: "Cleric",
        5: "Ranger"
    }

    chosen_class = class_mapping.get(class_choice, "Warrior")
    
    # Create and display the character
    character = Character(name, chosen_class)
    character.display_character()

if __name__ == "__main__":
    create_character()