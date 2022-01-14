import docker

def client() -> docker.DockerClient: 
    return docker.from_env()