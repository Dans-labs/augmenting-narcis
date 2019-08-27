#!/bin/bash

mkdir $(pwd)/data
datadir=$(pwd)/data/original
mkdir $datadir
curl https://dataverse.nl/api/access/datafile/15230 -o $datadir/harvest.2019-05-15.gz
curl https://digitalscience.figshare.com/ndownloader/files/15167609 -o $datadir/grid.zip
curl https://dataverse.nl/api/access/datafile/15236 -o $datadir/DOIboost2017.tar.gz
curl https://dataverse.nl/api/access/datafile/15237 -o $datadir/DOIboost2018.tar.gz
curl https://dataverse.nl/api/access/datafile/16269 -o $datadir/../elastic.tar.gz
gzip -cd $datadir/harvest.2019-05-15.gz > $datadir/harvest.2019-05-15 
cd $datadir/../data
gzip -cd ./elastic.tar.gz|tar xvf - 
rm ./elastic/data/nodes/0/node.lock
# Upload NARCIS data to MongoDB
docker exec augmenting-narcis_web_1 '/narcis/bin/importmetadata.py'
# Then upload the same data to elastic
docker exec augmenting-narcis_web_1 '/narcis/bin/metadata2elastic.py'
