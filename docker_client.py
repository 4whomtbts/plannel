import paramiko
import json
import requests
import logging
from container import Container

class DockerClient:

    def __init__(self, host, sudoer_id, sudoer_pwd, servers):
        self.cli = paramiko.SSHClient()
        self.cli.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.host = "210.94.223.123"
        self.cli.close()
        pass

    def get_all_containers_in_cluster(self):
        self.cli.connect("210.94.223.123", port=8081, username="4whomtbts", password="Hndp^(%#9!Q")
        stdin, stdout, stderr = self.cli.exec_command("sudo docker ps -a | sed -n '2,$p' | awk '{print $1}'", get_pty=True)
        lines = stdout.readlines()
        stderr_lines = stderr.readlines()
        for line in lines:
            line = line.replace('\r', '').replace('\n', '')
            inspect_stdin, inspect_stdout, inspect_stderr =\
                self.cli.exec_command("sudo docker inspect {}".format(line), get_pty=True)
            print("inspect_stdout = ", inspect_stdout.readlines())


    def get_all_containers(self, port, all):
        url = "http://{}:{}/v1.40/containers/json?all=true".format(self.host, port)
        res = requests.get(url)
        if res.status_code is not requests.codes.ok:
            logging.error("get_all_containers 요청 실패 : url - %s, status_code - %s", url, res.status_code)
        print(res.text)
        res_dict_list = json.loads(res.text)
        cont_list = []
        for cont_json in res_dict_list:
            container_id = cont_json["Id"]
            image = cont_json["Image"]
            name = cont_json["Names"]
            state = cont_json["State"]
            status = cont_json["Status"]
            created_at = cont_json["Created"]
            cmd = cont_json["Command"]
            cont = Container(container_id, image, cmd, created_at, state, status, None, name)
            cont_list.append(cont)
            print(cont)
            #print(self.get_container_log(port, cont.container_id))
        pass

    def get_container_log(self, port, container_id):
        url = "http://{}:{}/v1.40/containers/{}/logs?stdout=true&stderr=true".format(self.host, port, container_id)
        res = requests.get(url)
        if res.status_code is not requests.codes.ok:
            logging.error("get_container_log 요청 실패 : url - %s, status_code - %s, res_text - %s", url, res.status_code, res.text)
            return "로그 획득에 실패했습니다"
        return res.text
    ''' 
    example : http://210.94.223.123:9599/v1.40/images/create?fromImage=alpine:latest 
    '''
    def pull_image(self, image_name, tag):
        pass

    """
    build image: https://docs.docker.com/engine/api/v1.40/#operation/ImageBuild
    """
    def build_image(self):
        pass