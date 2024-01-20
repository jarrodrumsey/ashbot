import unittest
from kanban import KanbanModule, KanbanItem

class TestKanbanModule(unittest.TestCase):

    def setUp(self):
        self.board = KanbanModule()
        # Generate Columns
        self.board.add_column("To Do")
        self.board.add_column("In Progress")
        self.board.add_column("Done")
        self.board.add_column("Extra")
        self.board.add_column("Needing Signatures")
        self.board.add_column("Early Concepts")

        # Generate Items
        self.board.add_item("To Do", KanbanItem("Task 1"))
        self.board.add_item("To Do", KanbanItem("Speak to Graphic Designer"))
        self.board.add_item("To Do", KanbanItem("Develop Gantt Chart"))
        self.board.add_item("In Progress", KanbanItem("Task 0"))
        self.board.add_item("In Progress", KanbanItem("Meet with Finance"))
        self.board.add_item("In Progress", KanbanItem("Develop Marketing"))
        self.board.add_item("Done", KanbanItem("Kick-off Meeting"))
        self.board.add_item("Done", KanbanItem("Initial Talks"))
        self.board.add_item("Early Concepts", KanbanItem("Recently Added Task"))

    def test_delete_column(self):
        self.board.delete_column("Extra")
        self.assertNotIn("Extra", self.board.columns)

    def test_delete_item(self):
        self.board.delete_item("Done", "Initial Talks")
        self.assertFalse(self.board.columns["Done"].isInside("Initial Talks"))

    def test_move_column(self):
        self.board.move_column("Needing Signatures", "Done")
        keys = list(self.board.columns.keys())
        self.assertEqual(keys.index("Needing Signatures") + 1, keys.index("Done"))

        self.board.move_column("Early Concepts", "To Do")
        keys = list(self.board.columns.keys())
        self.assertEqual(keys.index("Early Concepts") + 1, keys.index("To Do"))

    def test_move_item(self):
        self.board.move_item("Early Concepts", "Recently Added Task", "To Do")
        self.assertTrue(self.board.columns["To Do"].isInside("Recently Added Task"))
        self.assertFalse(self.board.columns["Early Concepts"].isInside("Recently Added Task"))

        self.board.move_item("To Do", "Recently Added Task", "To Do", "Speak to Graphic Designer")
        index = self.board.columns["To Do"].get_item_index("Recently Added Task")
        self.assertLess(index, self.board.columns["To Do"].get_item_index("Speak to Graphic Designer"))

        self.board.move_item("To Do", "Recently Added Task", "In Progress", "Develop Marketing")
        self.assertTrue(self.board.columns["In Progress"].isInside("Recently Added Task"))
        self.assertFalse(self.board.columns["To Do"].isInside("Recently Added Task"))

if __name__ == '__main__':
    unittest.main()