#!/usr/bin/env python3

# ~ Manages your player's food inventory.
# ~ Euh... I mean... Your kitchen's fridge and pantery.
# ~ Also ties in with your favorite recipes.

# ~ Author: CodeArtha
# ~ Code: https://github.com/codeartha/pantry-inventory
# ~ Tip the author: - BTC: 1G2J5DwfGFfBJbreLJrymTA5NXHu4Pya6i
# ~                 - ETH: 0xEbc563324d69448E2F039deDA838c3a8873B2d3B


# TO-DO: switch over to argparse someday
# Currently items quantities are handled in INT. One apple, one egg, one loaf of bread, one pack of sugar. Maybe someday change it to FLOATS? In any case the database stores them as REAL so decimals can be stored.


import sys
import sqlite3
import os


HELP_MESSAGE = '''
usage: inventory.py [-h] [add | remove | list] [amount] [itemname]

description:
Manages your player's food inventory.
Euh... I mean... Your kitchen's fridge and pantery.
Also ties in with your favorite recipes.

author: CodeArtha
code: https://github.com/CodeArtha/pantry-inventory

positional arguments:
    add         adds 'x' amount of 'item' to your inventory
    remove      removes 'x' amount of 'item' of your inventory
    list        show/list all your current inventory
    init        (re)create the database that stores your inventory

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
    if(os.path.isfile(DATABASE_FILE)):
        clear_terminal()
        print('Warning: The database file already exist. Going further will errase data.')
        print('Options:')
        print('1: Cancel, keep my data safe')
        print('2: Rebuild just the inventory database')
        print('3: Rebuild both inventory and recipes database')
        action = int(input('What do you want to do [1, 2, 3]? '))
        if(action == 1):
            print('Initialization cancelled...')
            return 1
        elif(action == 2):
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
        elif(action == 3):
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


def add_item(itm, increase_by):
    itm = itm.lower()
    increase_by = int(increase_by)
    
    connection, cursor = connect(DATABASE_FILE)
    
    cursor.execute("""SELECT quantity FROM items WHERE item = ?""", (itm,))
    print(cursor.fetchone())
    
    if(not bool(cursor.fetchone())):
        # The item doesn't exist yet
        try:
            cursor.execute("""INSERT INTO items (item, quantity) VALUES(?, ?)""", (itm, increase_by,))
            connection.commit()
        except:
            connection.rollback()
            raise RuntimeError("Failed to create new item and update it's amount")
        finally:
            close(connection)
            
    else:
        # Item already exist, update it's amount
        current_amount = cursor.fetchone()[0]
        
        if(int(current_amount) <= 0): # Shouldn't ever happen, but Todd Howard, you know...
            new_amount = increase_by
        else:
            new_amount = current_amount + increase_by

        try:
            cursor.execute("""UPDATE items SET quantity=? WHERE item=?""", (new_amount, itm,))
            connection.commit()
        except:
            connection.rollback()
            raise RuntimeError("Could not update value upon item addition")
        finally:
            close(connection)


def remove_item(itm, decrease_by):
    itm = itm.lower()
    decrease_by = int(decrease_by)
    
    connection, cursor = connect(DATABASE_FILE)
    
    cursor.execute("""SELECT quantity FROM items WHERE item = ?""", (itm,))
    current_amount = cursor.fetchone()[0]
    
    if(int(current_amount) >= decrease_by):
        new_amount = current_amount - decrease_by
    else:
        new_amount = 0
        print('Warning: tried to remove more {} than currently in possession. Caped amount at zero.'.format(itm))

    try:
        cursor.execute("""UPDATE items SET quantity=? WHERE item=?""", (new_amount, itm,))
        connection.commit()
    except:
        connection.rollback()
        raise RuntimeError("Could not update value upon item deletion")
    finally:
        close(connection)
    

def main(args):
    """ Parsing command line arguments """
    if(args[1] == 'add'):
        # Adding items to inventory
        try:
            qty = int(args[2])
            item = args[3]
            add_item(item, qty)
        except IndexError:
            print('Error: To add an item to your inventory you need to specify the amount and item name. How serendipitous...')
            print(HELP_MESSAGE)
        except ValueError:
            print('Error: The quantity specified is not a number.')
            print(HELP_MESSAGE)
        else:
            print('Successfully added {} {} to your inventory'.format(qty, args[3]))

                 
    elif(args[1] == 'remove'):
        # Remove items from inventory
        try:
            qty = int(args[2])
            item = args[3]
        except IndexError:
            print('Error: To remove an item from your inventory you need to specify the amount and item name. How serendipitous...')
            print(HELP_MESSAGE)
        except ValueError:
            print('Error: The quantity specified is not a number.')
            print(HELP_MESSAGE)
        else:
            print('Successfully removed {} {} to your inventory'.format(qty, args[3]))

            
    elif(args[1] == 'show' or args[1] == 'list'):
        # List content (items with qty > 0)
        print('Inventory content:')
        print('this: 4')
        print('that: 2')

    elif(args[1] == 'init' or args[1] == 'initialize'):
        initialize_database()

    elif(args[1] == '-h' or args[1] == '--help'):
        print(HELP_MESSAGE)
    else:
        # Default
        print(HELP_MESSAGE)


if __name__ == '__main__':
    main(sys.argv)
