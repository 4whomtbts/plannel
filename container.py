
class Container:

    def __init__(self, container_id, image, command, created, state, status, ports, name):
        self.container_id = container_id
        self.image = image
        self.command = command
        self.created = created
        self.state = state
        self.status = status
        self.ports = ports
        self.name = name
        pass

    def __str__(self):
        return "container_id : {}, name : {}, image : {}, cmd : {}, created : {}, state : {}".format(
              self.container_id, self.name, self.image, self.command, self.created, self.state)