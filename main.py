import paramiko
import configparser
import logging
import re
from server import Server
from docker_client import DockerClient

conf = configparser.ConfigParser()
conf.read("plannel_conf.ini")
conf_subject="plannel"
plannel_conf = conf[conf_subject]
VERSION = plannel_conf["version"]
SERVERS = plannel_conf["servers"]
server_url_list = SERVERS.split(",")
server_list = []
for hostAndPort in server_url_list:
    p = '(?:http.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'
    m = re.search(p, hostAndPort)
    host = m.group('host')
    port = m.group('port')
    if host == '' or port == '':
        logging.error("{} is invalid form of host:port string".format(hostAndPort))
        continue
    logging.info("{} is included to managed server list".format(hostAndPort))
    server = Server(host, port)
    server_list.append(server)

cli = DockerClient(server_list)
cli.get_all_containers_in_cluster()
#cli.get_all_containers(9599, True)