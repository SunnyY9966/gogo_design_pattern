class Component:
    def __init__(self, id, description):
        self.id = id
        self.description = description


class Composite(Component):
    parent: Component
    # children = []

    def __init__(self, id, description):
        super(Composite, self).__init__(id, description)
        self.children = list()

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
    root = None
    serialId = 0

    def __new__(self):
        if not MindMapModel.__single:
            MindMapModel.__single = object.__new__(self)
        return MindMapModel.__single

    def create_mind_map(self, desc):
        node_factory = SimpleNodeFactory()
        self.root = node_factory.create_node("root", 0, desc)

    def create_node(self, desc):
        self.serialId += 1
        node_factory = SimpleNodeFactory()
        return node_factory.create_node("node", self.serialId, desc)

    def insert_node(self, parent_id, node):
        if parent_id == 0:
            parent = self.root
        else:
            parent = self.search_node(parent_id, self.root.children)

        if parent is not None:
            node.set_parent(parent)
            parent.add_child(node)
            print("insert_node - parent: ", parent.id, " child id: ", node.id)

    def search_node(self, id, children):
        if not children:
            return None
        elif children[0].id == id:
            return children[0]
        else:
            return self.search_node(id, children[1:])


class SimpleNodeFactory:
    def create_node(self, type, newId, desc):
        if type == "root":
            return Composite(0, desc)
        elif type == "node":
            return Composite(newId, desc)
