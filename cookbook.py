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
