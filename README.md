# Description

A few python scripts to manage your personnal inventory and crafting recipes in this videogame that is living on this planet.

inventory.py manages your inventory
recipes.py manages your favorite crafting recipes

Both tie themselves together by using the same database.

# Getting started

## inventory.py

With this script you can add and remove items from your inventory as well as list what you currently have.

* Initialization

To start, you need to initialize the database that will store everything.
You would do this only once, the first time you run this program. Or to reset the data and start again from scratch.
Run:

> $ ./inventory [init | initialize]

The menu offers multiple options. You can either reset everything or just your inventory.
Reseting just the inventory will keep all your recipes untouched. That way you don't waste hours re-teaching them to the system.

* Managing items

Adding and removing items from your inventory is super easy. The command structure is as follows and is made to resemble a natural english phrase:

> $ ./inventory [add|remove] [amount] [itemname]

The [itemname] is matched "as is". Therefore it is probably wise for you to come up with some standardization rules. Don't bother with capital letters as everything is converted to lower case.

* Inventory contents

To display what's currently in your inventory use the following command:

> $ ./inventory show

## recipes.py

This script manages your favorite recipes. You can create recipes, browse them and select one you want to make.
Feeling a lack of inspiration? Ask for a random recipe.
Selecting a recipe will tell you what you are missing to craft it so that you can do some quick groceries afterwork on you way home to make the diner.
Crafting a recipe will remove the items from you inventory automatically.

* Create a new recipe

> $ ./recipes add

A menu will walk you through it's creation.
When specifying the ingredients keep in mind that their name should match the convention you use for items in your inventory so that they can work together nicely.

* Browsing recipes

> $ ./recipes showall

Displays a list of recipes with their ID. You can then see the ones that interest you with the following command:

> $ ./recipes show [ recipe id | "title"]

Showing a recipe will also display the items you lack to create it.

* Crafting

> $ ./recipes craft [# of portions] [ recipe id | "title"]

This will offer to remove the selected items from you inventory.

* Lack of inspiration?

> $ ./recipes random

This chooses a random recipe for you and displays it along with the missing items.

Don't feel like eating that? Too many missing items? Too long to cook?
Hit next for another random one.

# Donations

Any financial help is of course appreciated:

- BTC: 1G2J5DwfGFfBJbreLJrymTA5NXHu4Pya6i
- ETH: 0xEbc563324d69448E2F039deDA838c3a8873B2d3B

But more importantly do share your thaughts / suggestions with me so that I can improve this script over time





