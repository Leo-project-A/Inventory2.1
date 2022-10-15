
from inventory import Inventory, Item
import os
import json

from mainConstants import DATABASE_DIR

def convert_files(filepath_list: list[str]) -> list[Inventory]:
    my_list = []

    for item in filepath_list:
        object_dict = import_inventory(item)
        my_list.append(object_dict)
    return my_list

def construct_invOnject(jsonString: str):
    """creates and returns an Inventory obj from a JSON file string """
    for x,item in enumerate(jsonString['content']):
        # makes sure the items dictionaries also convert to items
        jsonString['content'][x] = Item(**item)
    return Inventory(**jsonString)

def import_inventory(filename: str) -> Inventory:
    """imports the inventory into an obj
    filename includes extention. exm: .json 
    
    CONSIDER: moving this inside Inventory() 
    another constructer Inventory.fromFile()"""
    try:
        with open(f"DBs/{filename}", 'r') as file:
            jsonData = json.load(file)
            return construct_invOnject(jsonData)
    except:
        print(f"failed to open the file: {filename}")
        return None

def create_invList():
    return convert_files(os.listdir(DATABASE_DIR))

def updateDirectory(inventory_list):
    directory_list = [item.split('.')[0] for item in os.listdir(DATABASE_DIR)]
    for item in inventory_list:
        if item.name in directory_list:
            export_inventory(item)
            directory_list.pop(directory_list.index(item.name))
        else:
            export_inventory(item)
    if directory_list:
        for item in directory_list:
            delete_inventory(item)

def export_inventory(inventory: Inventory) -> None:
    """updates the inventory FILE in the db directory
    type: the file format to save the inventory"""
    filepath = f"{DATABASE_DIR}/{inventory.name}.json"
    with open(filepath, 'w') as jsonFile:
        for x,item in enumerate(inventory.content):
            inventory.content[x] = item.__dict__
        inv = json.dumps(inventory.__dict__)
        jsonFile.write(inv)

def delete_inventory(inveontory_name: str):
    """deletes an inventory with the given string name.
    return: True if deleted succesfuly. else return False"""
    dir_list = os.listdir(DATABASE_DIR)
    for dir in dir_list:
        if dir.split('.')[0] == inveontory_name:
            os.remove(DATABASE_DIR + dir)
            return True
    return False

def save_shoplist(str_list: list[str], output_dir: str, filename: str) -> None:
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    with open(output_dir + filename, 'w') as file:
        for item in str_list:
            file.write(item + '\n')
