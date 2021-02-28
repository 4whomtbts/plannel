import configparser

class PlannelConfig:

    def __init__(self):
        self.conf = configparser.ConfigParser()
        self.conf.read("plannel_conf.ini")
        conf_subject = "plannel"
        plannel_conf = self.conf[conf_subject]
        self.VERSION = plannel_conf["version"]
        self.SERVERS = plannel_conf["servers"]
        self.SSH_PORTS = plannel_conf["ssh_ports"]
        self.DOCKER_PORTS = plannel_conf["docker_ports"]
        DOCKER_REQUEST_TIMEOUT_MS = "docker_request_timeout_ms"
        self.DOCKER_REQUEST_TIMEOUT_MS = 3000
        if DOCKER_REQUEST_TIMEOUT_MS in plannel_conf:
            self.DOCKER_REQUEST_TIMEOUT_MS = int(plannel_conf[DOCKER_REQUEST_TIMEOUT_MS])
        CONTAINER_LOG_FILE_PATH = "container_log_file_path"
        self.CONTAINER_LOG_FILE_PATH = "./"
        if CONTAINER_LOG_FILE_PATH in plannel_conf:
            self.CONTAINER_LOG_FILE_PATH = plannel_conf[CONTAINER_LOG_FILE_PATH]