import configparser
import logging
import re
from server import Server
from docker_client import DockerClient
from plannel_config import PlannelConfig

config = PlannelConfig()
server_host_list = config.SERVERS.split(",")
server_list = []
server_dict = dict()
for server in server_host_list:
    splitted = server.split(":")
    alias = splitted[0]
    host = splitted[1]
    server_info = dict()
    server_info["host"] = host
    server_dict[alias] = server_info

ssh_ports_list = config.SSH_PORTS.split(",")
for ssh_port in ssh_ports_list:
    splitted = ssh_port.split(":")
    alias = splitted[0]
    port = splitted[1]
    server_info = server_dict.get(alias)
    server_info["ssh_port"] = port

docker_ports_list = config.DOCKER_PORTS.split(",")
for docker_port in docker_ports_list:
    splitted = docker_port.split(":")
    alias = splitted[0]
    port = splitted[1]
    server_info = server_dict.get(alias)
    server_info["docker_port"] = port

'''
for hostAndPort in server_host_list:
    p = '(?:http.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'
    m = re.search(p, hostAndPort)
    host = m.group('host')
    port = m.group('port')
    if host == '' or port == '':
        logging.error("{} is invalid form of host:port string".format(hostAndPort))
        continue
    logging.info("{} is included to managed server list".format(hostAndPort))
'''
for alias in server_dict:
    info = server_dict.get(alias)
    new_server = Server(alias, info["host"], info["ssh_port"], info["docker_port"])
    logging.info("{} 가 관리대상 서버에 포함됩니다".format(new_server))
    server_list.append(new_server)

cli = DockerClient(config, server_list)
print(cli.get_all_containers_in_cluster())
cli.create_container("helloworld", server_list[0])
