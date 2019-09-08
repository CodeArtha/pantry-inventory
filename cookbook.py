#!/usr/bin/env python3

# ~ Manages your player's food inventory.
# ~ Euh... I mean... Your kitchen's fridge and pantry.
# ~ Also ties in with your favorite recipes.

# ~ Author: CodeArtha
# ~ Code: https://github.com/codeartha/pantry-inventory
# ~ Tip the author: - BTC: 1G2J5DwfGFfBJbreLJrymTA5NXHu4Pya6i
# ~                 - ETH: 0xEbc563324d69448E2F039deDA838c3a8873B2d3B


import sys
import os
import sqlite3

HELP_MESSAGE = '''
usage: recipe.py [-h | help] [command]

description:
Manages your favorite recipes. Proposes a random recipe when you lack inspiration.
Is tied to your inventory and can automatically remove the consumed items when you craft the recipe.

author: CodeArtha
code: https://github.com/CodeArtha/pantry-inventory

positional arguments (available commands):
    new [title]         interactive menu to create a new recipe
    edit [title]        edit an existing recipe
    remove [title]      removes a recipe from your cookbook
    rename [old] [new]  if you just want to change the title of a recipe
    listall             shows all the recipes stored in your cookbook
    listrandom          suggests 5 random recipes when lacking ideas
    craft [qty] [title] removes the items needed to craft that recipe 'qty' times from your inventory
    init                (re)create the database that stores your cookbook

optional arguments:
    -h, --help        shows this help message
'''


DATABASE_FILE = 'kitchen.sqlite3'


def clear_terminal():
    # Clears the current terminal OS independant
    os.system('cls' if os.name == 'nt' else 'clear')


def connect(sqlite_file):
    """ Make connection to an SQLite database file """
    try:
        conn = sqlite3.connect(sqlite_file)
        cur = conn.cursor()
    except sqlite3.Error as e:
        print('could not connect to database')
        print(e)
        conn.close()
        return 0
    else:
        return conn, cur


def close(conn):
    """ Commit changes and close connection to the database """
    conn.commit()
    conn.close()
    return 1


def initialize_database():
    if os.path.isfile(DATABASE_FILE):
        clear_terminal()
        print('Warning: The database file already exist. Going further will errase data.')
        print('Options:')
        print('1: Cancel, keep my data safe')
        print('2: Rebuild just the inventory database')
        print('3: Rebuild both inventory and recipes database')
        action = int(input('What do you want to do [1, 2, 3]? '))
        if action == 1:
            print('Initialization cancelled...')
            return 1
        elif action == 2:
            connection, cursor = connect(DATABASE_FILE)

            cursor.execute("""
                DROP TABLE IF EXISTS items
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS items(
                id INTEGER UNSIGNED PRIMARY KEY,
                item TEXT UNIQUE NOT NULL,
                quantity REAL)
            """)

            close(connection)
            return 1
        elif action == 3:
            connection, cursor = connect(DATABASE_FILE)

            cursor.execute("""DROP TABLE IF EXISTS items""")
            cursor.execute("""DROP TABLE IF EXISTS recipes""")
            cursor.execute("""DROP TABLE IF EXISTS ingredients""")

            connection.commit()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS items(
                id INTEGER UNSIGNED PRIMARY KEY,
                item TEXT UNIQUE NOT NULL,
                quantity REAL)
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS recipes(
                id INTEGER UNSIGNED PRIMARY KEY,
                title TEXT UNIQUE NOT NULL,
                type TEXT CHECK(type IN ('starter', 'main', 'dessert', 'snack')) NOT NULL DEFAULT 'dish',
                description TEXT,
                instructions TEXT)
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ingredients(
                id INTEGER UNSIGNED PRIMARY KEY,
                quantity REAL,
                item_id INTEGER UNSIGNED,
                recipe_id INTEGER UNSIGNED)
            """)

            close(connection)
            return 1
        else:
            print('Initialization cancelled...')
            return 1
    else:
        print('Initializing a new empty database to story your inventory and crafting recipes')
        connection, cursor = connect(DATABASE_FILE)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS items(
            id INTEGER UNSIGNED PRIMARY KEY,
            item TEXT UNIQUE NOT NULL,
            quantity REAL)
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recipes(
            id INTEGER UNSIGNED PRIMARY KEY,
            title TEXT UNIQUE NOT NULL,
            type TEXT CHECK(type IN ('starter', 'main', 'dessert', 'snack')) NOT NULL DEFAULT 'main',
            description TEXT,
            instructions TEXT)
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ingredients(
            id INTEGER UNSIGNED PRIMARY KEY,
            quantity REAL,
            item_id INTEGER UNSIGNED NOT NULL,
            recipe_id INTEGER UNSIGNED NOT NULL)
        """)

        close(connection)
    return 1


def save_recipe(rcp_dict):
    connection, cursor = connect(DATABASE_FILE)

    cursor.execute(
        """INSERT INTO recipes 
        (title, type, description, instructions) 
        VALUES(?,?,?,?)""", (
            rcp_dict['title'],
            rcp_dict['type'],
            rcp_dict['description'],
            rcp_dict['instructions'],
        )
    )

    cursor.execute("""SELECT id FROM recipes WHERE title = ?""", (rcp_dict['title'],))
    rcp_id = cursor.fetchone

    ingredients = rcp_dict['ingredients']
    for i in ingredients:
        amount = i[0]
        item = i[1]
        cursor.execute("""""")
        pass

    close(connection)
    return 1


def create_recipe(title=None):
    print("Creating a new recipe")
    print("=====================")

    if title is None:
        rcp_title = input("New recipe title: ")
    else:
        rcp_title = title

    rcp_type = ''
    while rcp_type not in {'starter', 'main', 'dessert', 'snack'}:
        rcp_type = input("Type of course (starter, main, dessert, snack): ")

    print("Ingredient list")
    print("===============")
    print("Normalize the amounts for a \'one person\'s\' dish")
    print("Enter the ingredients with the same name as in your inventory")
    print("Use the following format: [qty]<space>[ingredient_name_without_spaces]")
    print("When done, type END on a new line")
    print("===============")
    rcp_ingredients = []
    limit = 128
    while True:
        limit -= 1
        usr_input = input()

        if usr_input == "END":
            break
        elif limit <= 0:
            print("You reached the limit in the number of ingredients of this recipe")
            print("PS: What recipe requires more than 128 ingredients? Email me that ;)")
            break
        else:
            fragments = usr_input.split()
            #amount = float(fragments[0])
            #ingr_name = ''.join(fragments[1:]).lower()
            amount = fragments[0]
            ingr_name = fragments[1]
            tuple = (ingr_name, amount)
            print(tuple)
            rcp_ingredients.append(tuple)

    print("=================")
    print(rcp_ingredients)

    rcp_description = ''
    print("\nEnter a brief recipe description: (type 'END' on a new line when done)")
    while True:
        usr_input = input()
        if usr_input == "END":
            break
        else:
            rcp_description += usr_input + "\n"

    rcp_instructions = ''
    print("\nGive the instructions to prepare this dish: (type 'END' on a new line when done)")
    while True:
        usr_input = input()
        if usr_input == "END":
            break
        else:
            rcp_instructions += usr_input + "\n"

    clear_terminal()
    print("===================================")
    print("Review your recipe before saving it")
    print("===================================")
    print("Title: " + rcp_title)
    print("Type: " + rcp_type)
    print("Description: \n" + rcp_description)
    print("Ingredients: ")
    for i in rcp_ingredients:
        print("{}: {}".format(i[0], i[1]))
    print()
    print("Instructions: \n" + rcp_instructions)

    agree = input("Save this recipe? (yes/no) ").lower()
    if agree == "y" or agree == "yes":
        save_recipe({"title": rcp_title,
                     "type": rcp_type,
                     "desc": rcp_description,
                     "ingr": rcp_ingredients,
                     "inst": rcp_instructions
        })
        print("Recipe saved.")
    else:
        create_recipe()


def main(args):
    """ Parsing command line arguments """
    if args[1] == 'new':
        if len(args) == 3:
            create_recipe(args[2])
        else:
            create_recipe()

    elif args[1] == 'edit':
        pass
    elif args[1] == 'remove':
        pass
    elif args[1] == 'rename':
        pass
    elif args[1] == 'listall':
        pass
    elif args[1] == 'listrandom':
        pass
    elif args[1] == 'craft':
        pass
    elif args[1] == 'init' or args[1] == 'initialize':
        initialize_database()

    elif args[1] == '-h' or args[1] == '--help':
        print(HELP_MESSAGE)

    else:
        # Default
        print(HELP_MESSAGE)


if __name__ == '__main__':
    main(sys.argv)
