import re
import logging

class Server:

    def __init__(self, alias, host, ssh_port, docker_port):
        self.alias = alias
        self.host = host
        self.ssh_port = ssh_port
        self.docker_port = docker_port

    def __str__(self):
        return "alias - {}, host - {}, ssh_port - {}, docker_port - {}"\
            .format(self.alias, self.host, self.ssh_port, self.docker_port)
