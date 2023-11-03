class Node:
    def __init__(self, rushHourPuzzle, parent=None, action="", c=1, h=0, depth=0):
        self.state = rushHourPuzzle
        self.parent = parent
        self.action = action
        self.g = 0 if not self.parent else self.parent.g + c
        self.f = self.g + h
        self.depth = depth

    def getPath(self):
        states = []
        node = self
        while node is not None:
            states.append(node.state)
            node = node.parent
        return states[::-1]

    def getSolution(self):
        actions = []
        node = self
        while node is not None:
            actions.append(node.action)
            node = node.parent
        return actions[::-1]
