#!/usr/bin/env python3

# ~ Manages your player's food inventory.
# ~ Euh... I mean... Your kitchen's fridge and pantery.
# ~ Also ties in with your favorite recipes.

# ~ Author: CodeArtha
# ~ Code: https://github.com/codeartha/pantry-inventory
# ~ Tip the author: see github


# TO-DO: switch over to argparse someday

HELP_MESSAGE = '''
usage: inventory.py [-h] [add | remove | list] x item

description:
Manages your player's food inventory.
Euh... I mean... Your kitchen's fridge and pantery.
Also ties in with your favorite recipes.

author: CodeArtha
code: https://github.com/CodeArtha/pantry-inventory

positional arguments:
    add                adds 'x' amount of 'item' to your inventory
    remove            removes 'x' amount of 'item' of your inventory
    list            show/list all your current inventory
    initialize        (re)create the database that stores your inventory

optional arguments:
    -h, --help        shows this help message
'''

# Parsing command line arguments
if(args[1] == 'add'):
    # Adding items to inventory
    print('Added x amount of something to your inventory')
    
elif(args[1] == 'remove'):
    # Remove items from inventory
    print('Removed / consumed x amount of something')

elif(args[1] == 'show' or args[1] == 'list'):
    # List content (items with qty > 0)
    print('Inventory content:')
    print('this: 4')
    print('that: 2')

elif(args[1] == 'init' or args[1] == 'initialize'):
    print('Database initialized')

elif(args[1] == '-h' or args[1] == '--help'):
    print(HELP_MESSAGE)
else:
    # Default
    print(HELP_MESSAGE)
