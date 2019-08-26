#!/bin/bash

mkdir $(pwd)/data
datadir=$(pwd)/data/original
mkdir $datadir
wget https://dataverse.nl/api/access/datafile/15230 -O $datadir/harvest.2019-05-15.gz
wget https://digitalscience.figshare.com/ndownloader/files/15167609 -O $datadir/grid.zip
wget https://dataverse.nl/api/access/datafile/15236 -O $datadir/DOIboost2017.tar.gz
wget https://dataverse.nl/api/access/datafile/15237 -O $datadir/DOIboost2018.tar.gz
wget https://dataverse.nl/api/access/datafile/16269 -O $datadir/../elastic.tar.gz
gzip -cd $datadir/harvest.2019-05-15.gz > $datadir/harvest.2019-05-15 
cd $datadir/../data
gzip -cd ./elastic.tar.gz|tar xvf - 
rm ./elastic/data/nodes/0/node.lock
# Upload NARCIS data to MongoDB
docker exec augmenting-narcis_web_1 '/narcis/bin/importmetadata.py'
# Then upload the same data to elastic
docker exec augmenting-narcis_web_1 '/narcis/bin/metadata2elastic.py'
