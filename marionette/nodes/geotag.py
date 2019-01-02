from .node import Node
from .common import attributes





class Geotag(Node):

    def __init__(self, *, generic=None, name=None, id=None, data=None):

        self._name = name
        self._id = id
        self._data = data

        if generic:
            self._name = generic

    def __repr__(self):
        name, id, data = attributes(self)

        if name:
            return 'User(name=\'{}\')'.format(name)
        elif id:
            return 'User(id=\'{}\')'.format(id)
        elif data:
            return 'MediaUser(data=\'{...}\')'

    @property
    def name(self):
        name, id, data = attributes(self)

        if name:
            return name
        elif id:
            pass
        elif data:
            return data['user']['name']
        else:
            return False

    @property
    def id(self):
        name, id, data = attributes(self)
        if id:
            return id
        elif data:
            return data['user']['name']
        else:
            return False