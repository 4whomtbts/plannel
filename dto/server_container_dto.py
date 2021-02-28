from server import Server
from container import Container

class ServerContainerDTO:

    def __init__(self, server, containers):
        self.server = server
        self.containers = containers
