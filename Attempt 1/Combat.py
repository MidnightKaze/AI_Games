import random
import time

# --- PLAYER CLASS ---
class Player:
    def __init__(self, name, health, mana, attack, defense):
        self.name = name
        self.health = health
        self.mana = mana
        self.attack = attack
        self.defense = defense
        self.is_alive = True
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.is_alive = False
            print(f"{self.name} has been defeated!")
    
    def heal(self, amount):
        self.health += amount
        print(f"{self.name} heals for {amount} HP!")
    
    def attack_enemy(self, enemy):
        damage = random.randint(self.attack // 2, self.attack) - enemy.defense
        damage = max(0, damage)  # Ensure damage can't be negative
        print(f"{self.name} attacks {enemy.name} for {damage} damage!")
        enemy.take_damage(damage)
    
    def use_item(self, item, enemy=None):
        if item == "Health Potion":
            self.heal(30)
        elif item == "Mana Potion":
            self.mana += 20
            print(f"{self.name} restores 20 mana!")
        elif item == "Fireball" and self.mana >= 10:
            self.mana -= 10
            damage = random.randint(20, 40)
            print(f"{self.name} casts Fireball on {enemy.name} for {damage} damage!")
            enemy.take_damage(damage)

    def choose_action(self, enemy):
        print("\nChoose an action:")
        print("1. Attack")
        print("2. Use Item")
        print("3. Defend")
        action = input("Enter the number of your choice: ")
        
        if action == '1':
            self.attack_enemy(enemy)
        elif action == '2':
            self.use_item("Health Potion")
        elif action == '3':
            self.defend()
    
    def defend(self):
        print(f"{self.name} defends!")
        self.defense += 5  # Temporary defense boost
        time.sleep(1)  # Delay for combat rhythm
        self.defense -= 5  # Reset defense after turn

# --- ENEMY CLASS ---
class Enemy:
    def __init__(self, name, health, attack, defense):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.is_alive = True
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.is_alive = False
            print(f"{self.name} has been defeated!")
    
    def attack_player(self, player):
        damage = random.randint(self.attack // 2, self.attack) - player.defense
        damage = max(0, damage)
        print(f"{self.name} attacks {player.name} for {damage} damage!")
        player.take_damage(damage)

    def choose_action(self, player):
        action = random.choice(["Attack", "Defend", "Special"])
        
        if action == "Attack":
            self.attack_player(player)
        elif action == "Defend":
            self.defend()
        elif action == "Special":
            self.special_attack(player)
    
    def defend(self):
        print(f"{self.name} defends!")
        self.defense += 3
        time.sleep(1)
        self.defense -= 3

    def special_attack(self, player):
        print(f"{self.name} uses a special attack!")
        damage = random.randint(20, 50)
        player.take_damage(damage)

# --- COMBAT SYSTEM ---
class Combat:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
    
    def battle(self):
        while self.player.is_alive and self.enemy.is_alive:
            print(f"\n{self.player.name} HP: {self.player.health}  |  {self.enemy.name} HP: {self.enemy.health}")
            
            # Player's Turn
            self.player.choose_action(self.enemy)
            if not self.enemy.is_alive:
                break

            # Enemy's Turn
            self.enemy.choose_action(self.player)
            if not self.player.is_alive:
                break

            time.sleep(1)

        if self.player.is_alive:
            print(f"\n{self.player.name} has won the battle!")
        else:
            print(f"\n{self.enemy.name} has won the battle!")

# --- MAIN GAME LOOP ---
def main():
    player = Player(name="Hero", health=100, mana=50, attack=25, defense=10)
    enemy = Enemy(name="Goblin", health=80, attack=20, defense=5)

    print("A wild Goblin appears!")
    combat = Combat(player, enemy)
    combat.battle()

if __name__ == "__main__":
    main()