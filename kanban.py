class KanbanItem():
    def __init__(self, name, column=None):
        self.name = name
        self.column = column
    
    def set_column(self, column):
        self.column = column
        
    def __str__(self):
        return f"{self.name}";

class KanbanColumn():
    def __init__(self, name):
        self.name = name
        self.items = []

    def get_item_index(self, item_name):
        return next((i for i, item in enumerate(self.items) if (item.name == item_name)), None)
    
    def isInside(self, item_name):
        return any(item.name == item_name for item in self.items)
            
    def add_item(self, item):
        item.column = self
        self.items.append(item)
    
    def delete_item(self, item_name):
        self.items.remove(self.items[self.get_item_index(item_name)])
     
    def __str__(self):
        return f"Column: {self.name}, Items: {[str(item) for item in self.items]}";
               
class KanbanModule():
    def __init__(self):
        self.object_operations = ["add", "delete", "move", "select", "rename"];
        self.item_types = ["column", "item"]
        self.columns = {}
        self.log = ""
    
    def add_column(self, column_name):
        self.columns[column_name] = KanbanColumn(column_name);
    
    def delete_column(self, column_name):
        if column_name in self.columns:
            self.columns.pop(column_name)
            self.log = ""
        else:
            self.log = "delete_column function: Referenced column does not exist."
    
    def add_item(self, column_name, item):
        if column_name in self.columns:
            self.columns[column_name].add_item(item)
            self.log = ""
        else:
            self.log = "add_item function: Referenced column or item does not exist."
    
    def delete_item(self, column_name, item_name):
        if column_name in self.columns and self.columns[column_name].isInside(item_name):
            self.columns[column_name].delete_item(item_name)
            self.log = ""
        else:
            self.log = "delete_item function: Referenced column or item does not exist."
        
    #   !kanban   move    {column/item} {name} to {column/item} {object_to_place_object_next_to}
    def move_column(self, column_name, new_next_column_name):

        # TODO: Ignore if moving action wouldn't actually cause a change.
        if (column_name in self.columns) and (new_next_column_name in self.columns):

            # The column will be moved such that it is the column just before the second column mentioned
            current_column = self.columns.pop(column_name)
            
            # Determine new position of the column (just before the second column name given)
            # and then place it within a list copy of the dictionary, then update the dictionary
            # with a dictionary conversion of the list. (Maintaining new order)

            new_position = list(self.columns.keys()).index(new_next_column_name)
            items_list = list(self.columns.items())
            items_list.insert(new_position, (column_name, current_column))
            self.columns = dict(items_list)
            
            self.log = ""
        else:
            self.log = "Referenced column does not exist."

    def move_item(self, column_name, item_name, next_column_name, next_item_name=None):
        
        valid_current = (column_name in self.columns) and self.columns[column_name].isInside(item_name)
        valid_next = next_column_name in self.columns and self.columns[next_column_name].isInside(next_item_name)

        if valid_current and valid_next:
            
            current_column = self.columns[column_name]
            current_list = current_column.items
            current_index = current_column.get_item_index(item_name) #   Get index of the object in the array
            
            new_column = self.columns[next_column_name]
            new_list = new_column.items
              
            if(next_item_name): # If the user tries to add an item into an item, the item will be appended such that it is the item just before the second item mentioned
                new_position = self.columns[next_column_name].get_item_index(next_item_name)
                new_list.insert(new_position, current_list.pop(current_index))
         
            else: # If the user tries to move an item into a column, the item will be appended as the last item of the column
                new_list.append(current_list.pop(current_index))
                
            self.log = ""
        else:
            self.log = "move_item function: Referenced column or item does not exist."
            
    def rename_column(self, column_name, new_column_name):
        if(column_name in self.columns):
            # TODO: Implement renaming function: Should not be able to rename column to have same name as a different

            position = list(self.columns.keys()).index(column_name)
            
            current_column = self.columns.pop(column_name)
            current_column.name = new_column_name
            
            column_list = list(self.columns.items())
            
            column_list.insert(position, (new_column_name, current_column))
            self.columns = dict(column_list)

        else:
            self.log = "TODO: rename_column function: Referenced column does not exist."
            
    def rename_item(self, column_name, item_name, new_item_name):
        if(column_name in self.columns) and self.columns[column_name].isInside(item_name):
            
            # Duplicate tasks are possible here by design. Might update to be a dictionary later to get rid of this feature.
            col = self.columns[column_name]
            index = col.get_item_index(item_name)
            col.items[index].name = new_item_name
            
        else:
            self.log = "TODO: rename_item function: Referenced column or item does not exist." 
            
    def __str__(self):
        return '\n'.join(str(column) for column in self.columns.values())

    def execute(self, message):
        #   Break down message into arguments corresponding to user's intended Kanban operation
        args = message.content.split()
        #   TODO: Use self.log somewhere in message        


        #   Command Syntax: !kanban {add/delete/move/select/rename} {column/item} {object_name} {new_name/adjacent_object_in_the_case_of_moving}

        #   ==================================================================================================
        #   Scenario: !kanban   add     {column/item} {name} in {column/item}
        #   TODO: Add the user's object (either a column or an item in a column) to the table.

            #   If the user tries to add an item into a column, the item will be appended as the last item of the column

            #   If the user tries to add a column into an item, the column will be added such that it is the column just after the column containing the item

            #   If the user tries to add a column into a column, the column will be added such that it is the column just after the second column mentioned

            #   If the user tries to add an item into an item, the item will be appended such that it is the item just after the second item mentioned




        #   ==================================================================================================
        #   Scenario: !kanban   delete  {column/item} {name} {column}
        #   TODO: Delete the user's object (either a column or an item in a column)
    
            #   If the user deletes an item that doesn't exist, say object not found.

            #   If the user deletes a column that doesn't exist, say object not found.

            #   If the user deletes a column, request secondary confirmation
                #   If the user accepts; delete column and all objects in column

                #   If the user declines; Say action aborted.


        #   ==================================================================================================
        #   Scenario: !kanban   move    {column/item} {name} to {column/item} {object_to_place_object_next_to}
        #   TODO: Move the user's object (either a column or an item in the column) to (next to another column or just after an item somewhere else in the table)
        
            #   If the user tries to move an item that doesn't exist, say object not found.

            #   If the user tries to move a column that doesn't exist, say object not found.

            #   If the user tries to move an item into a column, the item will be appended as the last item of the column

            #   If the user tries to move a column into an item, the column will be moved such that it is the column just after the column containing the item

            #   If the user tries to move a column into a column, the column will be moved such that it is the column just after the second column mentioned

            #   If the user tries to add an item into an item, the item will be appended such that it is the item just after the second item mentioned

        #   ==================================================================================================
        #   Scenario: !kanban   rename  {column/item} {name} {new_name}

# Test

board = KanbanModule()

# Generate Columns
print('Pretest - Generating Columns\n')
board.add_column("To Do")
board.add_column("In Progress")
board.add_column("Done")
board.add_column("Extra")
board.add_column("Needing Signatures")
board.add_column("Early Concepts")

# Generate Items
print('Pretest - Generating Items\n')
board.add_item("To Do", KanbanItem("Task 1"))
board.add_item("To Do", KanbanItem("Speak to Graphic Designer"))
board.add_item("To Do", KanbanItem("Develop Gantt Chart"))
board.add_item("In Progress", KanbanItem("Task 0"))
board.add_item("In Progress", KanbanItem("Meet with Finance"))
board.add_item("In Progress", KanbanItem("Develop Marketing"))
board.add_item("Done", KanbanItem("Kick-off Meeting"))
board.add_item("Done", KanbanItem("Initial Talks"))
board.add_item("Early Concepts", KanbanItem("Recently Added Task"))

print(board)

# Delete "Extra" column
print('\nTest - Delete "Extra" column\n')
board.delete_column("Extra");
print(board)

# Delete Initial talks item
print('\nTest - Delete "Initial Talks" task from "Done" column\n')
board.delete_item("Done", "Initial Talks");
print(board)

# Move "Needing Signatures" column just before "Done" column
print('\nTest - Move "Needing Signatures" column just before "Done" column\n')
board.move_column("Needing Signatures", "Done")
print(board)

# Move "Early Concepts" column to the start
print('\nTest - Move "Early Concepts" column to the start\n')
board.move_column("Early Concepts", "To Do")
print(board)

# Move "Recently Added Task" from "Early Concepts" to "To Do" column
print('\nTest - Move "Recently Added Task" from "Early Concepts" column to "To Do" column\n')
board.move_item("Early Concepts", "Recently Added Task", "To Do")
print(board)

# Move "Recently Added Task" from place in "To Do" column to before "Speak to Graphic Designer" task column
print('\nTest - Move "Recently Added Task" from place in "To Do" column to before "Speak to Graphic Designer" task column\n')
board.move_item("To Do", "Recently Added Task", "To Do", "Speak to Graphic Designer")
print(board)

# Move "Recently Added Task" from place in "To Do" column to before "Speak to Graphic Designer" task column
print('\nTest - Move "Recently Added Task" from place in "To Do" column to before "Develop Marketing" task in "In Progress" column\n')
board.move_item("To Do", "Recently Added Task", "In Progress", "Develop Marketing")
print(board)

