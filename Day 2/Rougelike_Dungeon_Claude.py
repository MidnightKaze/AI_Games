import random
import time
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Character:
    name: str
    race: str
    char_class: str
    health: int
    max_health: int
    mana: int
    max_mana: int
    strength: int
    defense: int
    magic: int
    inventory: List[str]
    spells: List[str]
    level: int
    exp: int

class Game:
    def __init__(self):
        self.races = {
            "human": {"health": 100, "mana": 50, "strength": 5, "defense": 5, "magic": 5},
            "kitsune": {"health": 80, "mana": 80, "strength": 4, "defense": 4, "magic": 8},
            "oni": {"health": 120, "mana": 30, "strength": 8, "defense": 6, "magic": 2},
            "tengu": {"health": 90, "mana": 60, "strength": 6, "defense": 4, "magic": 6},
            
            # New Races
            "yurei": {"health": 60, "mana": 100, "strength": 3, "defense": 3, "magic": 10},
            "kappa": {"health": 110, "mana": 40, "strength": 7, "defense": 6, "magic": 3},
            "raijin": {"health": 90, "mana": 70, "strength": 5, "defense": 5, "magic": 7},
            "nekomata": {"health": 70, "mana": 80, "strength": 4, "defense": 5, "magic": 9}
        }
        
        self.classes = {
            "samurai": {"health": 20, "mana": 0, "strength": 4, "defense": 3, "magic": 0, "spells": []},
            "onmyoji": {"health": 0, "mana": 30, "strength": 0, "defense": 1, "magic": 5, "spells": ["Fireball", "Lightning", "Spirit Ward"]},
            "ninja": {"health": 10, "mana": 10, "strength": 3, "defense": 2, "magic": 2, "spells": ["Smoke Screen", "Shadow Strike"]},
            "monk": {"health": 15, "mana": 15, "strength": 2, "defense": 4, "magic": 3, "spells": ["Healing Prayer", "Divine Protection"]},
            
            # New Classes
            "shugenja": {"health": 10, "mana": 40, "strength": 1, "defense": 2, "magic": 6, "spells": ["Earth Blessing", "Wind Blast", "Purify"]},
            "ronin": {"health": 25, "mana": 5, "strength": 5, "defense": 4, "magic": 1, "spells": []},
            "yamabushi": {"health": 20, "mana": 20, "strength": 3, "defense": 3, "magic": 4, "spells": ["Mountain Strength", "Sacred Flame"]},
            "kabuki": {"health": 15, "mana": 25, "strength": 2, "defense": 3, "magic": 5, "spells": ["Illusion Dance", "Spirit Mask"]}
        }

        
        self.enemies = {
            "Yokai": {"health": 80, "strength": 8, "defense": 6, "exp": 20},
            "Evil Spirit": {"health": 60, "strength": 6, "defense": 4, "exp": 15},
            "Corrupted Samurai": {"health": 100, "strength": 12, "defense": 8, "exp": 30},
            "Demon": {"health": 150, "strength": 14, "defense": 10, "exp": 40},
            
            # New Enemies
            "Oni Warrior": {"health": 120, "strength": 15, "defense": 10, "exp": 45},
            "Tsuchigumo": {"health": 90, "strength": 9, "defense": 7, "exp": 25},
            "Jorogumo": {"health": 70, "strength": 10, "defense": 5, "exp": 35},
            "Karakasa Obake": {"health": 50, "strength": 5, "defense": 3, "exp": 10},
            "Noppera-bo": {"health": 80, "strength": 6, "defense": 4, "exp": 20},
            "Yuki-onna": {"health": 100, "strength": 12, "defense": 8, "exp": 35},
            "Nurarihyon": {"health": 200, "strength": 20, "defense": 12, "exp": 60},
            "Gashadokuro": {"health": 250, "strength": 18, "defense": 15, "exp": 70}
        }

        
        self.player = None
        self.current_floor = 1
        self.story_progress = 0
        
    def clear_screen(self):
        print("\n" * 50)
        
    def slow_print(self, text):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(0.02)
        print()

    def create_character(self):
        self.clear_screen()
        self.slow_print("Welcome to the Shadows of Edo...")
        self.slow_print("\nIn an ancient Japan where yokai and humans coexist,")
        self.slow_print("darkness threatens to consume the land.")
        self.slow_print("\nFirst, tell me your name, brave warrior:")
        
        name = input("> ")
        
        self.clear_screen()
        self.slow_print("\nChoose your race:")
        for race in self.races:
            print(f"\n{race.title()}:")
            for stat, value in self.races[race].items():
                print(f"  {stat}: {value}")
                
        while True:
            race_choice = input("\nEnter your race choice: ").lower()
            if race_choice in self.races:
                break
            print("Invalid choice. Please try again.")
            
        self.clear_screen()
        self.slow_print("\nChoose your class:")
        for cls in self.classes:
            print(f"\n{cls.title()}:")
            for stat, value in self.classes[cls].items():
                if stat != "spells":
                    print(f"  {stat}: {value}")
                else:
                    print(f"  spells: {', '.join(value)}")
                    
        while True:
            class_choice = input("\nEnter your class choice: ").lower()
            if class_choice in self.classes:
                break
            print("Invalid choice. Please try again.")
            
        # Calculate total stats
        base_stats = self.races[race_choice].copy()
        class_stats = self.classes[class_choice].copy()
        spells = class_stats.pop("spells")
        
        for stat in base_stats:
            if stat in class_stats:
                base_stats[stat] += class_stats[stat]
                
        self.player = Character(
            name=name,
            race=race_choice,
            char_class=class_choice,
            health=base_stats["health"],
            max_health=base_stats["health"],
            mana=base_stats["mana"],
            max_mana=base_stats["mana"],
            strength=base_stats["strength"],
            defense=base_stats["defense"],
            magic=base_stats["magic"],
            inventory=["Healing Potion", "Mana Potion"],
            spells=spells,
            level=1,
            exp=0
        )
        
    def combat_round(self, enemy: Dict):
        enemy_health = enemy["health"]
        enemy_name = next(name for name, stats in self.enemies.items() if stats == enemy)
        
        while enemy_health > 0 and self.player.health > 0:
            self.clear_screen()
            print(f"\nBattle with {enemy_name}")
            print(f"\nYour HP: {self.player.health}/{self.player.max_health}")
            print(f"Your MP: {self.player.mana}/{self.player.max_mana}")
            print(f"Enemy HP: {enemy_health}/{enemy['health']}")
            
            print("\nActions:")
            print("1. Physical Attack")
            print("2. Use Spell")
            print("3. Use Item")
            print("4. Try to Run")
            
            choice = input("\nChoose your action (1-4): ")
            
            if choice == "1":
                damage = max(0, self.player.strength - enemy["defense"])
                enemy_health -= damage
                self.slow_print(f"\nYou attack for {damage} damage!")
                
            elif choice == "2" and self.player.spells:
                print("\nAvailable Spells:")
                for i, spell in enumerate(self.player.spells, 1):
                    print(f"{i}. {spell} (10 MP)")
                    
                spell_choice = input("\nChoose a spell (or 0 to go back): ")
                if spell_choice.isdigit() and 0 < int(spell_choice) <= len(self.player.spells):
                    if self.player.mana >= 10:
                        spell = self.player.spells[int(spell_choice) - 1]
                        damage = self.player.magic * 2
                        enemy_health -= damage
                        self.player.mana -= 10
                        self.slow_print(f"\nYou cast {spell} for {damage} damage!")
                    else:
                        self.slow_print("\nNot enough mana!")
                        continue
                        
            elif choice == "3":
                print("\nInventory:")
                for i, item in enumerate(self.player.inventory, 1):
                    print(f"{i}. {item}")
                    
                item_choice = input("\nChoose an item to use (or 0 to go back): ")
                if item_choice.isdigit() and 0 < int(item_choice) <= len(self.player.inventory):
                    item = self.player.inventory.pop(int(item_choice) - 1)
                    if item == "Healing Potion":
                        heal = 30
                        self.player.health = min(self.player.max_health, self.player.health + heal)
                        self.slow_print(f"\nYou heal for {heal} HP!")
                    elif item == "Mana Potion":
                        mana = 20
                        self.player.mana = min(self.player.max_mana, self.player.mana + mana)
                        self.slow_print(f"\nYou restore {mana} MP!")
                continue
                
            elif choice == "4":
                if random.random() < 0.4:
                    self.slow_print("\nYou successfully fled!")
                    return True
                else:
                    self.slow_print("\nCouldn't escape!")
            
            # Enemy turn
            if enemy_health > 0:
                damage = max(0, enemy["strength"] - self.player.defense)
                self.player.health -= damage
                self.slow_print(f"\n{enemy_name} attacks you for {damage} damage!")
                
            time.sleep(1)
            
        if enemy_health <= 0:
            self.slow_print(f"\nYou defeated the {enemy_name}!")
            self.player.exp += enemy["exp"]
            if self.player.exp >= 100:
                self.level_up()
            return True
        return False
        
    def level_up(self):
        self.player.level += 1
        self.player.exp -= 100
        self.player.max_health += 10
        self.player.max_mana += 5
        self.player.strength += 2
        self.player.defense += 2
        self.player.magic += 2
        self.player.health = self.player.max_health
        self.player.mana = self.player.max_mana
        self.slow_print(f"\nLevel Up! You are now level {self.player.level}!")
        
    def explore_dungeon(self):
        while True:
            self.clear_screen()
            print(f"\nFloor {self.current_floor}")
            print(f"HP: {self.player.health}/{self.player.max_health}")
            print(f"MP: {self.player.mana}/{self.player.max_mana}")
            
            print("\nWhat would you like to do?")
            print("1. Move forward")
            print("2. Rest (restore some HP and MP)")
            print("3. Check inventory")
            print("4. Check status")
            print("5. Quit game")
            
            choice = input("\nEnter your choice (1-5): ")
            
            if choice == "1":
                if random.random() < 0.7:  # 70% chance of encounter
                    enemy = random.choice(list(self.enemies.values()))
                    if not self.combat_round(enemy):
                        self.slow_print("\nGame Over!")
                        return
                else:
                    self.story_event()
                    
            elif choice == "2":
                heal = 20
                mana = 10
                self.player.health = min(self.player.max_health, self.player.health + heal)
                self.player.mana = min(self.player.max_mana, self.player.mana + mana)
                self.slow_print(f"\nYou rest and recover {heal} HP and {mana} MP.")
                time.sleep(1)
                
            elif choice == "3":
                self.clear_screen()
                print("\nInventory:")
                for item in self.player.inventory:
                    print(f"- {item}")
                input("\nPress Enter to continue...")
                
            elif choice == "4":
                self.clear_screen()
                print(f"\nName: {self.player.name}")
                print(f"Race: {self.player.race.title()}")
                print(f"Class: {self.player.char_class.title()}")
                print(f"Level: {self.player.level}")
                print(f"EXP: {self.player.exp}/100")
                print(f"HP: {self.player.health}/{self.player.max_health}")
                print(f"MP: {self.player.mana}/{self.player.max_mana}")
                print(f"Strength: {self.player.strength}")
                print(f"Defense: {self.player.defense}")
                print(f"Magic: {self.player.magic}")
                print("\nSpells:", ", ".join(self.player.spells) if self.player.spells else "None")
                input("\nPress Enter to continue...")
                
            elif choice == "5":
                self.slow_print("\nThank you for playing!")
                return
                
    def story_event(self):
        events = [
            "You find an ancient shrine. After paying respects, you feel invigorated. (+10 HP)",
            "A mysterious merchant appears, offering you a potion.",
            "You discover an old scroll containing magical wisdom. (+5 MP)",
            "The spirits of ancient warriors manifest, sharing their knowledge. (+1 Strength)",
            "You find a peaceful garden where you can meditate. (Fully restore MP)"
        ]
        
        event = random.choice(events)
        self.slow_print(f"\n{event}")
        
        if "HP" in event:
            self.player.health = min(self.player.max_health, self.player.health + 10)
        elif "merchant" in event:
            self.player.inventory.append("Healing Potion")
        elif "MP" in event:
            self.player.mana = min(self.player.max_mana, self.player.mana + 5)
        elif "Strength" in event:
            self.player.strength += 1
        elif "meditate" in event:
            self.player.mana = self.player.max_mana
            
        time.sleep(2)

def main():
    game = Game()
    game.create_character()
    game.explore_dungeon()

if __name__ == "__main__":
    main()