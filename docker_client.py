import paramiko
import json
import requests
import logging
from container import Container

class DockerClient:

    def __init__(self, server_list):
        self.cli = paramiko.SSHClient()
        self.cli.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.server_list = server_list
        self.cli.close()
        pass

    def get_all_containers_in_cluster(self):
        for server in self.server_list:
            self.get_all_containers(server.host, server.port)

    def get_all_containers(self, host, port):
        url = "http://{}:{}/v1.40/containers/json?all=true".format(host, port)
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