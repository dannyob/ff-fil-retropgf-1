#!/bin/env python
import requests
import os
import os
import subprocess
import json

def parse_go_mod_dependencies(go_mod_content):
    """
    Parses the go.mod file content and returns a list of dependencies.

    :param go_mod_content: Content of a go.mod file
    :return: List of dependencies
    """
    dependencies = []
    lines = go_mod_content.split('\n')
    inside_require_block = False
    for line in lines:
        line = line.strip()
        if line.startswith('require ('):
            inside_require_block = True
            continue
        if inside_require_block:
            if line.startswith(')'):
                inside_require_block = False
                continue
            if line:
                dependencies.append(line.split(' ')[0])
    return dependencies

tags = { 
        "corporate_sponsor" : ['uber', 'google', 'gogo', 'zondax', 'hashicorp'],
        "ecosystem_projects" : ['filecoin-project','ipfs','libp2p', 'multiformats', 'ipld'],
        "batteries_included" : ['golang.org', 'gotest.tools', 'golang' ]
        }

dependency_tags = {}

url = "https://raw.githubusercontent.com/filecoin-project/lotus/master/go.mod"
response = requests.get(url).content
dependencies = parse_go_mod_dependencies(response.decode('utf-8'))

for dependency in dependencies:
    dependency_tags[dependency] = []
    for tag, tag_values in tags.items():
        if any(tag_value in dependency for tag_value in tag_values):
            dependency_tags[dependency].append(tag)

tag_keys = list(tags.keys())
with open('dependencies.csv', 'w') as csv_file:
    csv_file.write('Dependency,' + ','.join(tag_keys) + '\n')
    for dependency, dependency_tag_list in dependency_tags.items():
        row = [dependency] + ['X' if tag in dependency_tag_list else '' for tag in tag_keys]
        csv_file.write(','.join(row) + '\n')

def checkout_and_get_go_mod_json():
    cache_dir = os.path.expanduser('~/.cache/lotus/')
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
        subprocess.run(['git', 'clone', '--depth', '1', 'https://github.com/filecoin-project/lotus/', cache_dir], check=True)
    os.chdir(cache_dir)
    subprocess.run(['git', 'submodule', 'update', '--init', '--recursive'], check=True)
    go_mod_json_output = subprocess.run(['go', 'mod', 'download', '-json'], stdout=subprocess.PIPE, check=True).stdout
    try:
        go_mod_json = json.loads(go_mod_json_output)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from go mod download -json: {e}")
        return None
    return go_mod_json

# Note: The rest of the existing code remains unchanged.
