import json
import random
import re
import sys
from datetime import datetime

# Stone Age Text Adventure Game
# A simple text-based game where the player explores a grid,
# collects materials, and crafts a knife to win.
# Player actions and stats are saved to a JSON file.


# Represents an item that can appear in a room
class Item:
    def __init__(self, description=""):
        self.potential_items = [
            "a pile of dirt",
            "a piece of flint",
            "a piece of granite",
            "a chunk of obsidian",
            "a rock of sandstone",
            "a wooden stick",
        ]
        self.description = description

    def set_item(self):
        self.description = random.choice(self.potential_items)

    def get_item(self):
        return self.description


# Represents a location containing terrain and items
class Room:
    def __init__(self):
        self.potential_terrains = [
            "a rocky terrain.",
            "a grassy terrain.",
            "a desert terrain.",
            "a swampy terrain.",
        ]
        self.terrain = ""
        self.items = []

    def set_random_terrain(self):
        self.terrain = random.choice(self.potential_terrains)

    def set_random_items(self):
        for _ in range(random.randint(1, 5)):
            item = Item()
            item.set_item()
            self.items.append(item)

    def get_items(self):
        return self.items

    def add_item(self, item_to_add):
        self.items.append(item_to_add)

    def remove_item(self, item_to_remove):
        for item in self.items:
            if item == item_to_remove:
                self.items.remove(item)

    def get_terrain(self):
        return self.terrain


# Represents the 3x3 game world and player movement
class Map:
    def __init__(self):
        self.topography = []
        self.position = {"first_index": 1, "second_index": 1}
        self.directions = ["north", "south", "east", "west", "n", "s", "e", "w"]

    # Generates a 3x3 grid of rooms and ensures required items exist to win
    def set_map(self):
        for _ in range(3):
            row = []
            for _ in range(3):
                room = Room()
                room.set_random_terrain()
                room.set_random_items()
                row.append(room)
            self.topography.append(row)

        # Checks if Game Map makes game unwinnable
        flint_count = 0
        obsidian_count = 0
        stick_count = 0
        for row in self.topography:
            for room in row:
                for item in room.get_items():
                    split_item = item.get_item().split(" ")
                    last_word = split_item[-1]
                    if "flint" == last_word:
                        flint_count += 1
                    elif "obsidian" == last_word:
                        obsidian_count += 1
                    elif "stick" == last_word:
                        stick_count += 1

        # Ensures enough materials exist on Gampe Map to make game winnable
        while flint_count < 2 and obsidian_count < 2:
            rand_row = random.randint(0, 2)
            rand_col = random.randint(0, 2)
            room = self.topography[rand_row][rand_col]
            if flint_count <= obsidian_count:
                item = Item("a piece of flint")
                room.add_item(item)
                flint_count += 1
            else:
                item = Item("a chunk of obsidian")
                room.add_item(item)
                obsidian_count += 1

        while stick_count < 1:
            rand_row = random.randint(0, 2)
            rand_col = random.randint(0, 2)
            room = self.topography[rand_row][rand_col]
            item = Item("a wooden stick")
            room.add_item(item)
            stick_count += 1

    # Moves the player in the given direction if within map bounds
    def set_player_position(self, direction):
        row = self.position["first_index"]
        col = self.position["second_index"]

        new_row, new_col = row, col
        if direction == "north" or direction == "n":
            print("Heading North...")
            new_row -= 1
        elif direction == "south" or direction == "s":
            print("Heading South...")
            new_row += 1
        elif direction == "west" or direction == "w":
            print("Heading West...")
            new_col -= 1
        else:
            print("Heading East...")
            new_col += 1

        if 0 <= new_row < len(self.topography) and 0 <= new_col < len(
            self.topography[0]
        ):
            self.position["first_index"] = new_row
            self.position["second_index"] = new_col
            return True
        else:
            print("You can't go that way. There's nothing but wilderness beyond")
            return False

    def get_player_position(self):
        row = self.position["first_index"]
        col = self.position["second_index"]
        room = self.topography[row][col]
        return room


# Stores player data (name, inventory, inputs, wins) and actions
class Player:
    def __init__(self):
        self.name = ""
        self.map = None
        self.inventory = {
            "dirt": 0,
            "flint": 0,
            "granite": 0,
            "obsidian": 0,
            "sandstone": 0,
            "stick": 0,
            "flint_knife_blade": 0,
            "obsidian_knife_blade": 0,
            "flint_knife": 0,
            "obsidian_knife": 0,
        }
        self.inputs = []
        self.wins = 0

    def get_name(self):
        return self.name

    def set_name(self):
        player_name = ""
        while not len(player_name):
            input_name = str(
                input(
                    "Please enter your name (any alphanumeric, min 3, max 12 characters): "
                )
            )
            if re.match(r"^[A-Za-z0-9]{3,12}$", input_name):
                player_name = input_name
            else:
                print("sorry, that name is not allowed.")
        self.name = player_name

    def set_map(self, map):
        self.map = map

    def increment_wins(self):
        self.wins += 1

    def get_wins(self):
        return self.wins

    # Resets Inventory between playthroughs
    def reset_inventory(self):
        for key in self.inventory:
            self.inventory[key] = 0

    def look_around(self, map):
        room = map.get_player_position()
        print(f"You find yourself in {room.get_terrain()}")
        if len(room.get_items()):
            print("On the ground, you see the following:")
            for item in room.get_items():
                print(f" - {item.get_item()}")
        else:
            print("There is nothing on the ground.")

    # Allows the player to pick up an item from the current room
    def take_item(self, map):
        room = map.get_player_position()
        items = room.get_items()
        valid_items = []

        for item in items:
            split_item = item.get_item().split(" ")
            last_word = split_item[-1]
            valid_items.append(last_word)

        user_input = str(input("Which item would you like to take?: ")).lower()

        if user_input in valid_items and user_input in list(self.inventory.keys()):
            print(f"Taking {user_input}...")
            self.set_inventory(user_input)
            for item in items:
                split_item = item.get_item().split(" ")
                last_word = split_item[-1]
                if user_input == last_word:
                    room.remove_item(item)
                    break
        else:
            print("Sadly, that item is not there for you to take.")

    def set_inventory(self, item):
        self.inventory[item] += 1

    def remove_inventory(self, item):
        self.inventory[item] -= 1

    def look_inventory(self):
        print("In your inventory, you see the following:")
        for key, value in self.inventory.items():
            print(f" - {value} of {key}")

    # Converts 2 flint or obsidian into a knife blade
    def knap_stone(self):
        has_materials_to_knap = False

        for key, value in self.inventory.items():
            if key == "flint" and value >= 2:
                print("Knapping flint blade...")
                has_materials_to_knap = True
                self.remove_inventory(key)
                self.remove_inventory(key)
                self.set_inventory("flint_knife_blade")
            elif key == "obsidian" and value >= 2:
                has_materials_to_knap = True
                print("Knapping obsidian blade...")
                self.remove_inventory(key)
                self.remove_inventory(key)
                self.set_inventory("obsidian_knife_blade")
            else:
                continue

        if not has_materials_to_knap:
            print(
                "Sorry, you need at least 2 chunks of flint or 2 chunks of obsidian to knap a blade..."
            )

    # Combines a blade and stick to create a knife (win condition)
    def make_knife(self):
        has_materials_to_make_knife = False
        has_enough_flint_blades = False
        has_enough_obsidian_blades = False

        for key, value in self.inventory.items():
            if key == "flint_knife_blade" and value >= 1:
                has_enough_flint_blades = True
            elif key == "obsidian_knife_blade" and value >= 1:
                has_enough_obsidian_blades = True

        for key, value in self.inventory.items():
            if key == "stick" and value >= 1:
                if has_enough_flint_blades or has_enough_obsidian_blades:
                    has_materials_to_make_knife = True

        if has_materials_to_make_knife:
            for key, value in self.inventory.items():
                if key == "flint_knife_blade" and value >= 1:
                    print("Making a flint knife...")
                    self.remove_inventory("flint_knife_blade")
                    self.set_inventory("flint_knife")
                elif key == "obsidian_knife_blade" and value >= 1:
                    print("Making a obsidian knife...")
                    self.remove_inventory("obsidian_knife_blade")
                    self.set_inventory("obsidian_knife")
            return True
        else:
            print("Sadly, you do not have the materials to make a knife yet.")
            return False

    def get_inputs(self):
        return self.inputs

    def set_inputs(self, input):
        self.inputs.append(input)

    # Saves player session data (name, inputs, wins, timestamp) to JSON file
    def save_stats(self):
        file_name = "stone_age.json"

        try:
            with open(file_name, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"players": []}

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        data["players"].append(
            {
                "name": self.get_name(),
                "wins": self.get_wins(),
                "inputs": self.get_inputs(),
                "date_time_played": timestamp,
            }
        )

        with open(file_name, "w") as file:
            json.dump(data, file, indent=4)


# Displays the game title and introduction
def display_title():
    print(
        "Welcome to Stone Age!\nA Text Adventure Game where you can travel around looking for stones and branches!\nThe point of the game is to knap a stone, find a stick, and make a knife!"
    )


# Displays available player commands
def print_help():
    print("Help message goes here")
    print("Player options:")
    print(" - Look Around: Type 'Look around' or 'L'")
    print(" - Look Inventory: Type 'Inventory' or 'I'")
    print(" - Go North: Type 'North' or 'N'")
    print(" - Go South: Type 'South' or 'S'")
    print(" - Go West: Type 'West' or 'W'")
    print(" - Go East: Type 'East' or 'E'")
    print(" - Take: Type 'Take' or 'T'")
    print(" - Knap Stone: Type 'Knap' or 'K'")
    print(" - Make Knife: Type 'Make' or 'M'")
    print("You can always type 'q' or 'quit' to quit.")


# Main game loop: processes player commands and actions
def parse_input(player, map):
    valid_directions = ["north", "south", "east", "west", "n", "s", "e", "w"]
    valid_inputs = [
        "q",
        "quit",
        "h",
        "help",
        "l",
        "look",
        "t",
        "take",
        "i",
        "inventory",
        "k",
        "knap",
        "m",
        "make",
    ] + valid_directions

    while True:
        user_input = str(input("What would you like to do?: ")).lower()
        if user_input in valid_inputs:
            player.set_inputs(user_input)
        else:
            print_help()
            continue

        if user_input == "q" or user_input == "quit":
            player.save_stats()
            break
        elif user_input == "h" or user_input == "help":
            print_help()
        elif user_input == "l" or user_input == "look":
            player.look_around(map)
        elif user_input == "t" or user_input == "take":
            player.take_item(map)
        elif user_input == "i" or user_input == "inventory":
            player.look_inventory()
        elif user_input == "k" or user_input == "knap":
            player.knap_stone()
        elif user_input == "m" or user_input == "make":
            won = player.make_knife()
            if won:
                print("\nCongratulations! You have conquered the Stone Age!")
                player.increment_wins()
                print(f"Total Wins: {player.get_wins()}")
                play_again = input("Would you like to play again? (y/n): ").lower()
                if play_again == "y":
                    return "restart"  # signal to restart the game
                else:
                    print("Thanks for playing!")
                    player.save_stats()
                    sys.exit()
        elif user_input in valid_directions:
            if map.set_player_position(user_input):
                player.look_around(map)


# Controls overall game flow and replay loop
def main():
    player = Player()
    player.set_name()
    while True:
        map = Map()
        map.set_map()
        player.set_map(map)

        print(f"Welcome to Stone Age, {player.get_name()}!")
        print(
            "Start your journey by looking around, type 'l' to look around or 'h' for help:"
        )

        result = parse_input(player, map)
        if result == "restart":
            print("\n--- Restarting the game ---\n")
            player.reset_inventory()
            continue
        else:
            break


if __name__ == "__main__":
    display_title()
    main()
    sys.exit()
