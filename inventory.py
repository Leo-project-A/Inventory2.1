
import os
import json
import time
import mainConstants

class Item():
    def __init__(self, id= None, name='item', category='misc', amount=1, priority= False) -> None:
        if id:
            self.id = id
        else:
            self.id = create_new_id()
        self.name = name
        self.category = category
        self.amount = amount
        self.priority = priority

    @classmethod
    def fromdict(self, dictionary: dict):
        """creates and returns an Item obj from a dictionary given"""
        return self(**dictionary)

    def printItem(self):
        """prints formated item details in a line.
        *FOR testing purposes. will be deleted*"""
        row_format ="{:>25}" * (len(self.__dict__.values()) - 1)
        print(row_format.format(self.name, self.category, self.amount, self.priority))

    def copy(self):
        """return a copy of the Item"""
        temp = Item()
        temp.id = self.id
        temp.name = self.name
        temp.category = self.category
        temp.amount = self.amount
        temp.priority = self.priority
        return temp

    def updateID(self, new_id):
        self.id = new_id
    def updateName(self, new_name):
        self.name = new_name
    def updateCategory(self, new_category):
        self.category = new_category
    def updateAmount(self, new_amount):
        self.amount = new_amount
    def updatePriority(self, new_priority):
        self.priority = new_priority


    # def update(self, changes):
    #     """updates the item with the changes from the dict. \n
    #     can be multiple changes at once
        
    #     {
    #         'name': 'new_name',
    #         'category': 'new_category'

    #         ...
    #     }"""
    #     for k,v in changes.items():
    #         self.__setattr__(k, v)

class Inventory():
    def __init__(self, id=None, name='inventory', description= '', content= []) -> None:
        if id:
            self.id = id
        else:
            self.id = str(time.time()).replace('.', '')
        if name == 'inventory':
            self.name = name + self.id
        else:
            self.name = name
        self.description = description
        self.content = content
    
    @classmethod
    def from_jasonFile(self, jsonData: str):
        """creates and returns an Inventory obj from a JSON file string
         CONSIDER : rewriting and use @overload __init__ for different constructors"""
        for x,item in enumerate(jsonData['content']):
            # makes sure the items dictionaries also convert to items
            # recently changed from: = Item(**item)
            jsonData['content'][x] = Item.fromdict(item)
        return self(**jsonData)

    def copy(self):
        """return a copy of the inventory"""
        temp = Inventory()
        temp.id = self.id
        temp.name = self.name
        temp.description = self.description
        for i in self.content:
            temp.content.append(i.copy())
        return temp

    def printInv(self, details= True, shop=False, filter= ''):
        """prints formated table of the inventory. \n
        *FOR testing purposes. will be deleted*"""
        if details:
            print(f"name: {self.name}")
            print(f"description: {self.description}")
            print("content:")

        if self.content:
            keys = list(self.content[0].__dict__.keys())[1:]
            row_format ="{:>25}" * len(keys)
            print(row_format.format(*keys))
            for item in self.content:
                if shop and item.amount != 0:
                    continue
                if filter and filter != item.category:
                    continue
                item.printItem()

    def addItem(self, new_item: Item):
        """add new_item to the end of this Inventory"""
        self.content.append(new_item)
        return True
    
    def addItems(self, items: list[Item]):
        """adds multiple items at the end of this Inventory"""
        for item in items:
            self.content.append(item)
        return True

    def getItem(self, name: str, pop=False):
        """returns the first Item with 'name' \n
        if pop=True, item also removed from Inventory"""
        for item in self.content:
            if item.name == name:
                if pop:
                    self.content.remove(item)
                return item
        return None

    def deleteItem(self, name: str):
        """removes 'name' from this Inventory"""
        return self.getItem(name, pop=True)

    def updateID(self, new_id):
        self.id = new_id
    def updateName(self, new_name):
        self.name = new_name
    def updateDescription(self, new_description):
        self.description = new_description
    def updateContent(self, new_content):
        self.content = new_content

    # def update(self, changes: dict):
    #     """updates the Inventory with the changes from the dict. \n
    #     can be multiple changes at once
        
    #     {
    #         'name': 'new_name',
    #         'description': 'new_description'

    #         ...
    #     }"""
    #     for k,v in changes.items():
    #         self.__setattr__(k, v)

    def updateItem(self, item: str, changes: dict):
        """updates the wanted 'item' with all the changes in the dictionary"""
        wanted_item = self.getItem(item)
        if wanted_item:
            wanted_item.update(changes)

    def getCategories(self):
        categories = set()
        for item in self.content:
            if type(item) == Item:
                categories.add(item.category)
        return list(categories)


def create_new_db(filename='inventory', desc='', type='json') -> Inventory:
    """creates a new inventory with the name given, saved with the file type. returns the object
    type: the file format to save the data
    returns: a DEFAULT Inventory obj"""
    new_inv = Inventory(name=filename, description=desc)
    if filename in getInventoryList():
        print("filename already exists, please choose another name")
        return None
    updateDB(new_inv, type)
    return new_inv
    # TO ADD: other file formats


def updateDB(inventory: Inventory, type= 'json') -> None:
    """updates the inventory FILE in the db directory
    type: the file format to save the inventory"""
    filepath = f"{mainConstants.DATABASE_DIR}/{inventory.name}.{type}"
    if type == 'json':
        with open(filepath, 'w') as jsonFile:
            for x,item in enumerate(inventory.content):
                inventory.content[x] = item.__dict__
            inv = json.dumps(inventory.__dict__)
            jsonFile.write(inv)


def import_inventory(filename: str) -> Inventory:
    """imports the inventory into an obj
    filename includes extention. exm: .json 
    
    CONSIDER: moving this inside Inventory() 
    another constructer Inventory.fromFile()"""
    ext = filename.split('.')[1]
    if ext == 'json':
        try:
            with open(f"{mainConstants.DATABASE_DIR}/{filename}", 'r') as file:
                jsonData = json.load(file)
                new_inv = Inventory.from_jasonFile(jsonData)
                return new_inv
        except:
            print(f"failed to open the file: {filename}")
            return None
    # TO ADD: for other file types
    elif ext == '':     
        pass

def delete_inventory(inveontory_name: str):
    """deletes an inventory with the given string name.
    return: True if deleted succesfuly. else return False"""
    dir_list = os.listdir(mainConstants.DATABASE_DIR)
    for dir in dir_list:
        if dir.split('.')[0] == inveontory_name:
            os.remove(mainConstants.DATABASE_DIR + dir)
            return True
    return False

def create_new_id():
    """creates a new UNIQUE id"""
    return str(time.time()).replace('.', '')

def getInventoryList():
    """returns full path with extention .json"""
    dir_list = os.listdir(mainConstants.DATABASE_DIR)
    return dir_list


