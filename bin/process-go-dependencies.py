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

cache_dir = os.path.expanduser('~/.cache/lotus/')
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)
    subprocess.run(['git', 'clone', '--depth', '1', 'https://github.com/filecoin-project/lotus/', cache_dir], check=True)
    os.chdir(cache_dir)
    subprocess.run(['git', 'submodule', 'update', '--init', '--recursive'], check=True)

go_mod_path = os.path.join(cache_dir, 'go.mod')
with open(go_mod_path, 'r') as go_mod_file:
    go_mod_content = go_mod_file.read()

dependencies = parse_go_mod_dependencies(go_mod_content)

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

# Note: The rest of the existing code remains unchanged.
