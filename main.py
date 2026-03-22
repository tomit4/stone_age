import json
import random
import re
import sys


class Item:
    def __init__(self):
        self.potential_items = [
            "a pile of dirt",
            "a piece of flint",
            "a piece of granite",
            "a chunk of obsidian",
            "a rock of sandstone",
            "a wooden stick",
        ]
        self.description = ""

    def set_item(self):
        self.description = random.choice(self.potential_items)

    def get_item(self):
        return self.description


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

    # TODO: After loop, ensure room has at least one item not currently in room
    def set_random_items(self):
        for _ in range(random.randint(1, 5)):
            item = Item()
            item.set_item()
            self.items.append(item)

    def get_items(self):
        return self.items

    def remove_item(self, item_to_remove):
        for item in self.items:
            if item == item_to_remove:
                self.items.remove(item)

    def get_terrain(self):
        return self.terrain


class Map:
    def __init__(self):
        self.topography = []
        self.position = {"first_index": 1, "second_index": 1}
        self.directions = ["north", "south", "east", "west", "n", "s", "e", "w"]

    def set_map(self):
        for _ in range(3):
            row = []
            for _ in range(3):
                room = Room()
                room.set_random_terrain()
                room.set_random_items()
                row.append(room)
            self.topography.append(row)

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


class Player:
    def __init__(self, map):
        self.map = map
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

    def look_around(self, map):
        room = map.get_player_position()
        print(f"You find yourself in {room.get_terrain()}")
        if len(room.get_items()):
            print("On the ground, you see the following:")
            for item in room.get_items():
                print(f" - {item.get_item()}")
        else:
            print("There is nothing on the ground.")

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

    #  def get_inventory(self):
    #  return self.inventory

    def look_inventory(self):
        print("In your inventory, you see the following:")
        for key, value in self.inventory.items():
            print(f" - {value} of {key}")

    def knap_stone(self):
        has_materials_to_knap = False

        for key, value in self.inventory.items():
            if key == "flint" and value == 2:
                print("Knapping flint blade...")
                has_materials_to_knap = True
                self.remove_inventory(key)
                self.remove_inventory(key)
                self.set_inventory("flint_knife_blade")
            elif key == "obsidian" and value == 2:
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

    def make_knife(self):
        has_materials_to_make_knife = False
        has_enough_flint_blades = False
        has_enough_obsidian_blades = False

        for key, value in self.inventory.items():
            if key == "flint_knife_blade" and value == 1:
                has_enough_flint_blades = True
            elif key == "obsidian_knife_blade" and value == 1:
                has_enough_obsidian_blades = True

        for key, value in self.inventory.items():
            if key == "stick" and value == 1:
                if has_enough_flint_blades or has_enough_obsidian_blades:
                    has_materials_to_make_knife = True

        if has_materials_to_make_knife:
            for key, value in self.inventory.items():
                if key == "flint_knife_blade" and value == 1:
                    print("Making a flint knife...")
                    self.remove_inventory("flint_knife_blade")
                    self.set_inventory("flint_knife")
                elif key == "obsidian_knife_blade" and value == 1:
                    print("Making a obsidian knife...")
                    self.remove_inventory("obsidian_knife_blade")
                    self.set_inventory("obsidian_knife")
        else:
            print("Sadly, you do not have the materials to make a knife yet.")


def display_title():
    print(
        "Welcome to Stone Age!\nA Text Adventure Game where you can travel around looking for stones and branches!\nThe point of the game is to knap a stone, find a stick, and make a knife!"
    )


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


def parse_input(player, map):
    valid_directions = ["north", "south", "east", "west", "n", "s", "e", "w"]

    while True:
        user_input = str(input("What would you like to do?: ")).lower()
        if user_input == "quit" or user_input == "q":
            break
        if user_input == "l" or user_input == "look":
            player.look_around(map)
        elif user_input == "t" or user_input == "take":
            player.take_item(map)
        elif user_input == "i" or user_input == "inventory":
            player.look_inventory()
        elif user_input == "k" or user_input == "knap":
            player.knap_stone()
        elif user_input == "m" or user_input == "make":
            player.make_knife()
        elif user_input in valid_directions:
            if map.set_player_position(user_input):
                player.look_around(map)
        else:
            print_help()
            continue


def main():
    map = Map()
    map.set_map()
    player = Player(map)

    player.set_name()
    print(f"Welcome to Stone Age, {player.get_name()}!")
    print(
        "Start your journey by looking around, type 'l' to look around or 'h' for help:"
    )

    parse_input(player, map)


if __name__ == "__main__":
    display_title()
    main()
    sys.exit()
