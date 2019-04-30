class Component:
    def __init__(self, id, description):
        self.id = id
        self.description = description


class Composite(Component):
    # parent: Component

    # children = []

    def __init__(self, id, description):
        super(Composite, self).__init__(id, description)
        self.children = []
        self.parent = None

    def add_child(self, node):
        self.children.append(node)
        print('children list: ' + str(self.children))

    def add_sibling(self, node):
        self.parent.add_child(node)

    def set_parent(self, parent):
        # assert isinstance(parent, Component)
        self.parent = parent

    def set_position(self, x, y):
        self.x = x
        self.y = y


class MindMapModel:
    __single = None
    _mindMap = {}
    root = None
    serialId = 0

    def __new__(self):
        if not MindMapModel.__single:
            MindMapModel.__single = object.__new__(self)
        return MindMapModel.__single

    def create_mind_map(self, desc):
        node_factory = SimpleNodeFactory()
        self.root = node_factory.create_node("root", 0, desc)
        self._mindMap[0] = self.root

    def create_node(self, desc):
        self.serialId += 1
        node_factory = SimpleNodeFactory()
        return node_factory.create_node("node", self.serialId, desc)

    def insert_node(self, parent_id, node):
        if parent_id == 0:
            parent = self.root
        else:
            parent = self._mindMap[parent_id]
            # parent = self.search_node(parent_id, self.root)

        if parent is not None:
            node.set_parent(parent)
            parent.add_child(node)
            self._mindMap[node.id] = node
            print("insert_node - parent id: ", parent.id, " child id: ", node.id,
                  " child len", len(parent.children))

    def search_node(self, id, root: Component) -> Component:

        if not root:
            return None
        elif root.id == id:
            return root
        else:
            for node in root.children:
                ans = self.search_node(id, node)
                if ans is not None:
                    return ans

    def traversal(self, root: Component):
        data = []

        if not root:
            return []
        else:
            data.append(root.id)
            for node in root.children:
                data = data + self.traversal(node)
        return data

    def get_ggm_format(self):
        data = []
        for node_id, node in self._mindMap.items():
            desc_and_children = "\"" + node.description + "\""
            if node.children:
                desc_and_children += " "

            desc_and_children += ' '.join(str(child.id) for child in node.children)
            tuple_data = (node_id, desc_and_children)
            print(tuple_data)
            data.append(tuple_data)

        return data

    def save_file(self, path):
        data = self.get_ggm_format()
        try:
            with open(path, 'w') as fp:
                fp.write('\n'.join('{} {}'.format(x[0], x[1]) for x in data))

        except Exception as e:
            print(e)


class SimpleNodeFactory:
    def create_node(self, type, new_id, desc):
        if type == "root":
            return Composite(0, desc)
        elif type == "node":
            return Composite(new_id, desc)
