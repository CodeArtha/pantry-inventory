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
    new                 interactive menu to create a new recipe
    edit [name]         edit an existing recipe
    remove [name]       removes a recipe from your cookbook
    rename [old] [new]  if you just want to change the title of a recipe
    listall             shows all the recipes stored in your cookbook
    listrandom          suggests 5 random recipes when lacking ideas
    craft [qty] [name]  removes the items needed to craft that recipe 'qty' times from your inventory
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
                type TEXT CHECK(type IN ('starter', 'dish', 'dessert', 'snack')) NOT NULL DEFAULT 'dish',
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
            type TEXT CHECK(type IN ('starter', 'dish', 'dessert', 'snack')) NOT NULL DEFAULT 'dish',
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

def main(args):
    """ Parsing command line arguments """
    if args[1] == 'new':
        pass
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
        pass
    elif args[1] == '-h' or args[1] == '--help':
        print(HELP_MESSAGE)
    else:
        # Default
        print(HELP_MESSAGE)

if __name__ == '__main__':
    main(sys.argv)
