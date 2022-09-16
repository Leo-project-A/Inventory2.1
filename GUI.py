
from PyQt5.QtWidgets import (
    QApplication, 
    QWidget,
    QDialog, 
    QComboBox, 
    QGroupBox, 
    QSpinBox, 
    QLineEdit, 
    QDialogButtonBox, 
    QVBoxLayout, 
    QHBoxLayout,
    QLabel, 
    QFormLayout,
    QCheckBox,
    QPushButton,
    QListWidget,
    QPlainTextEdit,
    QTableWidget,
    QTableWidgetItem,
    )
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
import sys
import inventory
import mainConstants

class mainWindow(QWidget): ### Tested
    def __init__(self):
        super(mainWindow, self).__init__()

        self.setWindowTitle("Inventory Manager")

        layout = QVBoxLayout()

        self.button_load = QPushButton("Inventories")
        self.button_load.clicked.connect(self.func_load)
        self.button_about = QPushButton("About")
        self.button_about.clicked.connect(self.func_about)
        self.button_exit = QPushButton("Exit")
        self.button_exit.clicked.connect(self.func_exit)
        layout.addWidget(self.button_load)
        layout.addWidget(self.button_about)
        layout.addWidget(self.button_exit)

        self.setLayout(layout)
        self.setFixedSize(400, layout.sizeHint().height())

    def func_load(self):
        self.new_window = InventoryWindow(self.pos())
        self.new_window.show()
        self.close()

    def func_about(self):
        self.new_window = aboutWindow(self.button_about.text(), self.pos())
        self.new_window.setWindowModality(Qt.ApplicationModal)
        self.new_window.show()

    def func_exit(self):
        self.close()

class InventoryWindow(QDialog): ### Tested
    def __init__(self, parent_pos):
        super(InventoryWindow, self).__init__()
        self.setWindowTitle("Inventories")
        self.setGeometry(parent_pos.x(), parent_pos.y(), 600, 200)
        
        self.invo_list = []                 # a list of the inventories list
        self.listWidget = QListWidget()     # the list widget for the gui
        self.refreshInvoList()

        # the button layout on the right
        verticalBoxLayout = QVBoxLayout()
        verticalBoxLayout.setAlignment(Qt.AlignTop)
        for text, slot in (
            ("Create New", self.createNew),
            ("Edit", self.edit),
            ("Remove", self.remove),
            ("View Inventory", self.viewInventory),
            ("Back", self.back)):

            button= QPushButton(text)
            verticalBoxLayout.addWidget(button)
            button.clicked.connect(slot)

        # the box layout - list on the left, buttons on the right
        horizontalBoxLayout = QHBoxLayout()
        horizontalBoxLayout.addWidget(self.listWidget)
        horizontalBoxLayout.addLayout(verticalBoxLayout)

        #set it as the main layout of this window
        self.setLayout(horizontalBoxLayout)

    def createNew(self):
        """open new UI for adding a new Inventory"""
        self.new_window = subInventoryWindow(self.pos(), "New Inventory")
        self.new_window.newObjCreated.connect(self.add_inventory)
        self.new_window.setWindowModality(Qt.ApplicationModal)
        self.new_window.show()

    def add_inventory(self, data):
        """creates a new inventory file in the dir
        with data input from the user"""
        if not data:
            return 
        for item in self.invo_list:
            if item.name == data['name']:
                print("name already exist, choose another  ****alert popup****")
                return
        inventory.create_new_db(filename=data['name'],desc=data['description'],type=data['type'])
        self.refreshInvoList()

    def edit(self):
        """edits the selected inventory"""
        if self.invo_list:
            self.selectedObj = self.invo_list.pop(self.listWidget.currentRow())

            self.new_window = subInventoryWindow(self.pos(), "Edit Inventory", self.selectedObj)
            self.new_window.newObjCreated.connect(self.edit_inventory)
            self.new_window.setWindowModality(Qt.ApplicationModal)
            self.new_window.show()

    def edit_inventory(self, data):
        if not data:
            self.invo_list.append(self.selectedObj)
            self.refreshInvoList()
            return 
        for item in self.invo_list:
            if item.name == data['name']:
                print("name already exist, choose another  ****alert popup****")
                self.invo_list.append(self.selectedObj)
                self.refreshInvoList()
                return

        inventory.delete_inventory(self.selectedObj.name)
        self.selectedObj.updateName = data['name']
        self.selectedObj.updateDescription = data['description']
        # self.selectedObj.update({
        #     'name': data['name'],
        #     'description': data['description']
        # })
        inventory.updateDB(self.selectedObj, data['type'])
        self.refreshInvoList()

    def remove(self):
        selectedObj = self.invo_list.pop(self.listWidget.currentRow())
        inventory.delete_inventory(selectedObj.name)
        self.refreshInvoList()

    def viewInventory(self):
        selectedObj = self.invo_list[self.listWidget.currentRow()]
        self.new_window = inventroyViewWindow(self.pos(), selectedObj)
        self.new_window.setWindowModality(Qt.ApplicationModal)
        self.new_window.show()

    def back(self):
        self.new_window = mainWindow()
        self.new_window.show()
        self.close()

    def refreshInvoList(self):
        """refreshes the self.listWidget with filenames.\n
        AND the self.invo_list of inventories\n
        after updates and changes"""
        self.listWidget.clear()
        self.invo_list: list[inventory.Inventory] = []
        dir_list = inventory.getInventoryList()
        if dir_list:
            for dir in dir_list:
                new_invoObj = inventory.import_inventory(dir)
                self.invo_list.append(new_invoObj)
                self.listWidget.addItem(new_invoObj.name)
        self.listWidget.setCurrentRow(0)

class inventroyViewWindow(QDialog):
    def __init__(self, parent_pos, selectedObj:inventory.Inventory=None):
        super(inventroyViewWindow, self).__init__()

        self.setWindowTitle("inventories")
        self.setGeometry(parent_pos.x(), parent_pos.y(), 800, 600)
        self.mainLayout = QVBoxLayout()
        # Set up the view and load the data
        self.view = QTableWidget()
        self.invoObj = selectedObj

        self.itemList = self.invoObj.content
        self.view.setColumnCount(len(mainConstants.ITEM_LABELS))
        self.view.setHorizontalHeaderLabels(mainConstants.ITEM_LABELS)
        self.itemCategories = self.invoObj.getCategories()
        for item in self.itemList:
            rows = self.view.rowCount()
            self.view.setRowCount(rows + 1)
            id_item = QTableWidgetItem(item.id)
            id_item.setFlags(Qt.ItemIsEnabled)
            self.view.setItem(rows, 0, id_item)
            name_item = QTableWidgetItem(item.name)
            name_item.setFlags(Qt.ItemIsEnabled)
            self.view.setItem(rows, 1, name_item)
            comboBox = QComboBox()
            comboBox.addItems(self.itemCategories)
            comboBox.setEditable(True)
            comboBox.InsertAtBottom
            comboBox.setCurrentText(item.category)
            self.view.setCellWidget(rows, 2, comboBox)

            amountSpinBar = QSpinBox()
            amountSpinBar.setValue(item.amount)
            self.view.setCellWidget(rows, 3, amountSpinBar)

            priorityBox = QComboBox()
            priorityBox.addItems(mainConstants.PRIORITIES)
            priorityBox.setCurrentText(item.priority)
            self.view.setCellWidget(rows, 4, priorityBox)
        self.view.resizeColumnsToContents()

        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignTop)

        for text, slot in (
            ("Save Inventory", self.saveInventory),
            ("Add New Item", self.createNewItem),
            ("Remove Item", self.removeItem),
            ("Back", self.close)):

            button= QPushButton(text)

            vbox.addWidget(button)
            button.clicked.connect(slot)

        hbox = QHBoxLayout()
        hbox.addWidget(self.view)
        hbox.addLayout(vbox)
        self.setLayout(hbox)

    def createNewItem(self):
        self.new_window = newItemWindow(self.pos(), self.itemCategories)
        self.new_window.setWindowModality(Qt.ApplicationModal)
        self.new_window.show()

    def saveInventory(self):
        rowCount = self.view.rowCount()
        columnCount = self.view.columnCount()

        for row in range(rowCount):
            self.itemList[row].updateCategory(self.view.cellWidget(row, 2).currentText())
            self.itemList[row].updateAmount(int(self.view.cellWidget(row, 3).text()))
            self.itemList[row].updatePriority(self.view.cellWidget(row, 4).currentText())
        inventory.updateDB(self.invoObj)
        self.close()


    def removeItem(self):
        pass


class subInventoryWindow(QDialog):
    newObjCreated = pyqtSignal(dict)

    def __init__(self, parent_pos, title, invoObj=None):
        super(subInventoryWindow, self).__init__()
        self.setWindowTitle(title)
        self.setGeometry(parent_pos.x(), parent_pos.y(), 600, 200)
        self.formGroupBox = QGroupBox()

        self.nameLineEdit = QLineEdit()
        self.typeLineEdit = QLineEdit()
        self.descriptionLineEdit = QPlainTextEdit()
        if invoObj:                     # currently editing existing inventory in this window
            self.nameLineEdit.setText(invoObj.name)
            self.typeLineEdit.setText('json')
            self.descriptionLineEdit.setPlainText(invoObj.description)
        else:                           # currently creating new inventory
            self.nameLineEdit.setText('default')
            self.typeLineEdit.setText('json')

        self.createForm()

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.getInfo)
        self.buttonBox.rejected.connect(self.back)
        mainLayout = QVBoxLayout()

        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(self.buttonBox)

        self.setLayout(mainLayout)

    def getInfo(self):
        # this will send the new item objet to the inventory
        new_invoDict = {
            'name': self.nameLineEdit.text(),
            'type': self.typeLineEdit.text(),
            'description': self.descriptionLineEdit.toPlainText(),
        }
        self.newObjCreated.emit(new_invoDict)
        self.close()
    
    @pyqtSlot()
    def back(self):
        self.newObjCreated.emit({})
        self.close()

    def createForm(self):
        layout = QFormLayout()
        layout.addRow(QLabel("Name"), self.nameLineEdit)
        layout.addRow(QLabel("File Type"), self.typeLineEdit)
        layout.addRow(QLabel("Description (Optional)"), self.descriptionLineEdit)

        self.formGroupBox.setLayout(layout)

class aboutWindow(QDialog):
    def __init__(self, titleName, parent_pos):
        super(aboutWindow, self).__init__()

        self.setWindowTitle(titleName)
        self.setGeometry(parent_pos.x(), parent_pos.y(), 300, 400)

class newItemWindow(QDialog):
    def __init__(self, parent_pos, categories):
        super(newItemWindow, self).__init__()

        self.setWindowTitle("Add Items")
        self.setGeometry(parent_pos.x(), parent_pos.y(), 300, 400)
        self.formGroupBox = QGroupBox("new item")

        self.nameLineEdit = QLineEdit()

        self.categoryComboBox = QComboBox()
        self.categoryComboBox.addItems(categories)
        self.categoryComboBox.setEditable(True)
        self.categoryComboBox.InsertAtBottom

        self.amountSpinBar = QSpinBox()

        self.priorityCheckBox = QCheckBox()

        self.createForm()

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.getInfo)
        self.buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()

        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(self.buttonBox)

        self.setLayout(mainLayout)

    def getInfo(self):
        # this will send the new item objet to the inventory
        new_itemObj = inventory.Item(
            id=inventory.create_new_id(),
            name=self.nameLineEdit.text(),
            category=self.categoryComboBox.currentText(),
            amount=self.amountSpinBar.text(),
            priority=self.priorityCheckBox.isChecked()
            )

    def createForm(self):
        layout = QFormLayout()
        layout.addRow(QLabel("Item"), self.nameLineEdit)
        layout.addRow(QLabel("Categoy"), self.categoryComboBox)
        layout.addRow(QLabel("Amount"), self.amountSpinBar)
        layout.addRow(QLabel("Priority Item"), self.priorityCheckBox)

        self.formGroupBox.setLayout(layout)


if __name__ == '__main__':

	app = QApplication([])
	window = mainWindow()
	window.show()
	sys.exit(app.exec())
