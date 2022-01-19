from pymongo import MongoClient
from pymongo.database import Database
from dotenv import load_dotenv
from typing import Tuple
import docker
import os
def get_mongo_client(name='pylineone', host=None, port=None, username=None, password=None) -> Tuple[MongoClient,Database]:
    load_dotenv()
    host = host or os.getenv("MONGO_HOST")
    port = port or os.getenv("MONGO_PORT")
    username = username or os.getenv("MONGO_USER")
    password = password or os.getenv("MONGO_PASS")

    client = MongoClient(host=host,
                        port=int(port),
                        username=username,
                        password=password
                        )
    return client, client[name]

def pull_docker_image():
    client = docker.from_env()
    if 'python:latest' not in (i.tags for i in client.images.list()):
        client.images.pull('python')

def get_detached_container():
    client = docker.from_env()
    return client.containers.run('python', detach=True)


def run_script(script):
    client = docker.from_env()
    return client.containers.run('python', script, remove=True)