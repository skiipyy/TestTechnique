import yaml

from src.graph import generate_json_graph

with open('./config/file_to_process.yaml') as yaml_file:
    config = yaml.safe_load(yaml_file)

generate_json_graph(
    config['drugs']['path'],
    config['clinical_trials']['path'],
    config['pubmeds']['path'],
    config['output']['path']
)