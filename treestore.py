from typing import List, Dict
import json


class Node:
    def __init__(self, id: int | str, value: Dict):
        self.id = id
        self.value = value
        self.children = []

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

    def __repr__(self):
        return self.__str__()


class TreeStore:

    def __init__(self, items: List[Dict]):
        self.items = items
        self.tree = dict()
        self.__create_tree()

    def __create_tree(self):

        for item in self.items:
            new_node = Node(
                id=item.get('id'),
                value=item
            )
            root = self.tree.get('root')
            if not root:
                self.tree['root'] = new_node
            else:
                self.__traverse(
                    root,
                    lambda node: node.children.append(
                        new_node
                    ) if node.id == item['parent'] else None
                )

    def __traverse(self, root: Node, callback):
        def walk(node):
            callback(node)
            for child in node.children:
                walk(child)
        walk(root)

    def __search_children(self, node: Node, id: int | str) -> Node | None:
        for item in node.children:
            if item.id == id:
                return item
            else:
                result = self.__search_children(item, id)
                if result is not None:
                    return result
        return None

    def __search_parents(self, node, all_parents: list) -> List[Node] | None:
        parent = self.__get_node(node.value['parent'])
        if parent:
            all_parents.append(parent)
            if parent.value['parent']:
                self.__search_parents(
                    node=parent,
                    all_parents=all_parents
                )

    def __get_node(self, id: int | str) -> Node | None:
        root = self.tree.get('root')
        return root if root.id == id else self.__search_children(root, id)

    def get_all(self) -> List[Dict]:
        return self.items

    def get_item(self, id: str | int):
        node = self.__get_node(id)
        return node.value if node else None

    def get_children(self, id: str | int):
        node = self.__get_node(id)
        return [item.value for item in node.children] if node else None

    def get_all_parents(self, id: str | int):
        initial_tree_node = self.__get_node(id)
        all_parents = []
        if initial_tree_node:
            self.__search_parents(initial_tree_node, all_parents)
        return [item.value for item in all_parents]
