INVENTORY_PATH = "inventoryDB.json"
DATABASE_DIR = 'DBs/'
SHOP_DIR = 'shopping/'
SHOP_SUFFIX = 'shoplist.txt'

ITEM_LABELS = ["id", "name", "category", "amount", "priority"]
PRIORITIES = ['low', 'HIGH']


about_text = '''An inventory system.  
Create and edit an inventory for your home/office/wearhouse

1. Create an inventory
2. Add items
3. review and update stocks, to know which items are running low
4. edit the inventory

Author: Leonid Sobol - leonis313@gmail.com
Project Link: https://github.com/Leo-project-A/Inventory2.1
'''

patch_notes = '''
- 2.1.3 -

-Added the option to export the shopping list for any inventory
    -Saves the items in the inventory with amount = 0 in a text file. 
    -Directory: 'shopping/'

- 2.1.2 -

-Reworked the inventory object managemnt 
-Added item creation and editing
-Added confirmation window when deleting files
    -inventory and item
-Added About page
-Added example inventories

- 2.1 -

-Fixed program crashing after creating new Inventory
-Fixed conflicting Object types while editing the inventory

-Added conversion_module

'''