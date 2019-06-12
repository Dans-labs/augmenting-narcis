echo 'Creating data folder structure..'
mkdir $(pwd)/data
mkdir $(pwd)/data/original
datadir=$(pwd)/data/original

echo 'Downloading subsets of DOIBoost..'
wget https://dataverse.nl/api/access/datafile/15236 -O $datadir/doiboost-2017.tar.gz
wget https://dataverse.nl/api/access/datafile/15237 -O $datadir/doiboost-2018.tar.gz

echo 'Unpacking the archives..'
tar -xvzf $datadir/doiboost-2017.tar.gz -O > $datadir/doiboost-2017.json
tar -xvzf $datadir/doiboost-2018.tar.gz -O > $datadir/doiboost-2018.json

echo 'Adding the data to elasticsearch..'
curl -s -XPOST localhost:9201/_bulk --data-binary @doiboost-2017.json
curl -s -XPOST localhost:9201/_bulk --data-binary @doiboost-2018.json

echo 'Done.'
