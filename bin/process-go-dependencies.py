#!/bin/env python
import requests

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

url = "https://raw.githubusercontent.com/filecoin-project/lotus/master/go.mod"
response = requests.get(url).content
dependencies = parse_go_mod_dependencies(response.decode('utf-8'))

# Example usage: Print the list of dependencies
for dep in dependencies:
    print(dep)

# use the devil's regexp to pull out lines describing dependencies
