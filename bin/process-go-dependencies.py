#!/bin/env python
import requests
import os
import subprocess
import json

cache_dir = os.path.expanduser('~/.cache/lotus/')

tags = { 
        "corporate_sponsor" : ['uber', 'google', 'gogo', 'zondax', 'hashicorp'],
        "ecosystem_projects" : ['filecoin-project','ipfs','libp2p', 'multiformats', 'ipld'],
        "batteries_included" : ['golang.org', 'gotest.tools', 'golang' ]
        }

def install_locally():
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
        subprocess.run(['git', 'clone', '--depth', '1', 'https://github.com/filecoin-project/lotus/', cache_dir], check=True)
        os.chdir(cache_dir)
        subprocess.run(['git', 'submodule', 'update', '--init', '--recursive'], check=True)

def parse_go_mod_dependencies(go_mod_path):
    """
    Parses the go.mod file content and returns a list of dependencies.

    :param go_mod_path: path of go.mod
    :return: List of dependencies
    """

    with open(go_mod_path, 'r') as go_mod_file:
        go_mod_content = go_mod_file.read()

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

def get_go_mod_download_json():
    """
    Changes to the cached lotus directory, runs `go mod download -json`, and returns the parsed JSON.

    :return: Parsed JSON output from `go mod download -json`
    """
    os.chdir(cache_dir)
    go_mod_download_output = subprocess.check_output(['go', 'mod', 'download', '-json'])
    json_objects = json.loads('[' + go_mod_download_output.decode('utf-8').replace('}\n{', '},{') + ']')
    return json_objects


dependency_tags = {}

go_mod_path = os.path.join(cache_dir, 'go.mod')
dependencies = parse_go_mod_dependencies(go_mod_path)

for dependency in dependencies:
    dependency_tags[dependency] = []
    for tag, tag_values in tags.items():
        if any(tag_value in dependency for tag_value in tag_values):
            dependency_tags[dependency].append(tag)

tag_keys = list(tags.keys())

print(get_go_mod_download_json())

with open('dependencies.csv', 'w') as csv_file:
    csv_file.write('Dependency,' + ','.join(tag_keys) + '\n')
    for dependency, dependency_tag_list in dependency_tags.items():
        row = [dependency] + [tag if tag in dependency_tag_list else '' for tag in tag_keys]
        csv_file.write(','.join(row) + '\n')

