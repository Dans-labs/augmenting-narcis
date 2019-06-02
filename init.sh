#!/bin/bash

# Upload NARCIS data to MongoDB
docker exec augmenting-narcis_web_1 '/narcis/bin/importmetadata.py'
# Then upload the same data to elastic
docker exec augmenting-narcis_web_1 '/narcis/bin/metadata2elastic.py'
