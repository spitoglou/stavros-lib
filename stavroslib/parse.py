from io import TextIOWrapper
import yaml


def read_yaml(file: str) -> dict:
    stream: TextIOWrapper = open(file, 'r', encoding='utf8')
    return yaml.load(stream, Loader=yaml.FullLoader)
