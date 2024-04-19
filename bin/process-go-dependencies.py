#!/bin/env python
import requests

url = "https://raw.githubusercontent.com/filecoin-project/lotus/master/go.mod"
response = requests.get(url).content

# use the devil's regexp to pull out lines describing dependencies
