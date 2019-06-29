# Description

A few python scripts to manage your personnal inventory and crafting recipes in this videogame that is living on this planet.

inventory.py manages your inventory
recipes.py manages your favorite crafting recipes

Both tie themselves together by using the same database.

# Usage

With the inventory script you can add and remove items from your inventory as well as list what you currently have.

* initializing your inventory (do this only the first time you run this program or to start all over again):

> $ ./inventory initialize

* adding/removing items to your inventory

> $ ./inventory [add|remove] [amount] [itemname]

* list inventory

> $ ./inventory show

* create a new recipe

> $ ./recipes add

* craft a recipe (offers to remove the items from inventory)

> $ ./recipes craft [name | id]

* list recipes

> $ ./recipes listall

* select a random recipe (for those evenings where you lack creativity)

> $ ./recipes random

# Donations

Any financial help is of course appreciated:
BTC: 1G2J5DwfGFfBJbreLJrymTA5NXHu4Pya6i
ETH: 0xEbc563324d69448E2F039deDA838c3a8873B2d3B

But more importantly do share your thaughts / suggestions with me so that I can improve this script over time





