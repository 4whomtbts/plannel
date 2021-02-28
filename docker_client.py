import paramiko
import secrets
import json
import requests
import datetime
import logging
import concurrent.futures
import os
from container import Container
from dto import server_container_dto


class DockerClient:

    def __init__(self, config, server_list):
        self.config = config
        self.sudoer_id = os.environ.get("ID")
        self.sudoer_pwd = os.environ.get("PWD")
        self.cli = paramiko.SSHClient()
        self.cli.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.server_list = server_list
        self.cli.close()
        pass

    def get_all_containers_in_cluster(self):
        cluster_server_containers = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            get_cont_futures = {executor.submit(self.get_all_containers, server):
                          server for server in self.server_list}
        for future in concurrent.futures.as_completed(get_cont_futures):
            server = get_cont_futures[future]
            try:
                data = future.result()
                if data is not None:
                    cluster_server_containers.append(
                        server_container_dto.ServerContainerDTO(server, data))
            except Exception as e:
                logging.error("클러스터 내의 호스트 %s:%s 의 컨테이너 획득에 실패했습니다 : %s",
                              server.host, server.port, e)
        return cluster_server_containers

    def get_all_containers(self, server):
        host = server.host
        docker_port = server.docker_port

        url = "http://{}:{}/v1.40/containers/json?all=true".format(host, docker_port)
        timeout = self.config.DOCKER_REQUEST_TIMEOUT_MS / 1000
        try:
            res = requests.get(url=url, timeout=timeout)
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
            return cont_list

        except requests.exceptions.ConnectionError as e:
            logging.error("{}:{} 에 연결하는데 실패했습니다 : {}".format(host, docker_port, e))
        except requests.exceptions.Timeout as e:
            logging.error("{}:{} 의 컨테이너 리스트 요청 중 timeout 이 발생했습니다 : {}".format(host, docker_port, e))
        except requests.exceptions.RequestException as e:
            logging.error("{}:{} 의 컨테이너 리스트 요청 중 예외가 발생했습니다 : {}".format(host, docker_port, e))
        return None

    def get_container_log(self, server, container_id):
        host = server.host
        docker_port = server.docker_port

        url = "http://{}:{}/v1.40/containers/{}/logs?stdout=true&stderr=true".format(host, docker_port, container_id)
        res = requests.get(url)
        if res.status_code is not requests.codes.ok:
            logging.error("get_container_log 요청 실패 : url - %s, status_code - %s, res_text - %s", url, res.status_code,
                          res.text)
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

    def create_container(self, user, server):
        cont_name = "{}-{}".format(user, secrets.token_hex(8))
        now = datetime.datetime.now()
        formatted = now.strftime("%Y%m%d:%H%M%S")
        try:
            self.cli.connect("210.94.223.123", port=8088, username=self.sudoer_id, password=self.sudoer_pwd)
        except Exception as e:
            raise Exception("{} 서버의 ssh 연결 중 오류가 발생하였습니다 : {}".format(server, e))
        run_cmd = "sudo docker run -d --name {} dguailab/ailab_base:1.0"\
            .format(cont_name)
        stdin, stdout, stderr = self.cli.exec_command(run_cmd, get_pty=True)
        create_output = stdout.readlines()
        create_err = stderr.readlines()
        if create_err is not None and len(create_err) > 0:
            f = open("{}-err-create-{}".format(cont_name, formatted), 'w')
            for err in create_err:
                f.write(err)
            f.close()
            raise Exception("컨테이너 {} 생성 중 오류가 발생했습니다 : {}".format(cont_name, create_err))
        f = open("{}-create-{}".format(cont_name, formatted), 'w')
        for line in create_output:
            f.write(line)
        f.close()
        logging.info("컨테이너 %s 가 생성되었습니다", cont_name)