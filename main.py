import paramiko
from docker_client import DockerClient

cli = DockerClient("210.94.223.123", "4whomtbts", "Hndp^(%#9!Q", "")
#cli.get_all_containers_in_cluster()
cli.get_all_containers(9599, True)