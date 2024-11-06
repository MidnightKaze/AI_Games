import time

def slow_print(text, delay=1):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay / 50)
    print()
 

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