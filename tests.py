import unittest
from treestore import TreeStore
from constants import items


class TestTreeStore(unittest.TestCase):
    def setUp(self):
        self.items = items
        self.treeStore = TreeStore(self.items)

    def test_get_all(self):
        self.assertEqual(self.treeStore.get_all(), self.items)

    def test_get_item(self):
        self.assertEqual(self.treeStore.get_item(1),
                         {'id': 1, 'parent': 'root'})
        self.assertIsNone(self.treeStore.get_item(0))

    def test_get_children(self):
        children = self.treeStore.get_children(2)
        self.assertTrue(all(child['parent'] == 2 for child in children))

    def test_get_all_parents(self):
        parents = self.treeStore.get_all_parents(9)
        self.assertTrue(
            all(parent['id'] in {1, 2, 4, 8} for parent in parents))


if __name__ == '__main__':
    unittest.main()
