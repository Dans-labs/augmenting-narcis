# augmenting-narcis
## Assessment for NARCIS Publication Information Enrichment

## Handy links for the project
#### Trello
https://trello.com/b/ZitfLTe0
#### Google Drive
The drive has the information about the complete project, without source code, and also some Elasticsearch indices.

https://drive.google.com/drive/folders/19IUE0X9BmP6FPM0T5Rv7qQBZ4eYXvWkB?usp=sharing

## File locations
There are a few locations for the new files. The import files for MongoDB and Elasticsearch have been added to narcisweb/bin/, together with createacd.py. This file creates the new author-country dataset. The rest of the code is written in jupyter notebooks and they can be found in notebooks/persistent/. 

## Running the code
The import scripts can be run when the DOIBoost2017, DOIBoost2018 and GRID datasets have been downloaded and unzipped in /data/orginal/. These are very basic scripts based on importmetadata.py and metadata2elastic.py. The script that creates the author-country dataset has been commented and all notebooks have extended documentation and comments. The notebooks should therefore be self explainatory. 

### Downloads
Download NARCIS data from https://dataverse.nl/dataset.xhtml?persistentId=hdl:10411/8H4QSU in the current folder (augmenting-narcis)
#### Grid
https://www.grid.ac/downloads
#### DOIBoost
https://zenodo.org/record/1438356#.XPTbxS-B2qA
#### Crossref Dump
https://github.com/greenelab/crossref/tree/master/data/mongo-export
https://archive.org/download/crossref_doi_dump_201809

# Subsets
Get subset of publications from 2017 (NARCIS)
```
cat ./data/original/harvest.2019-05-15 |grep '"date": \["2017'|grep 'info:eu-repo/semantics/article'
```

### Initialization
All data should be uploaded in MongoDB and Elastic before you can use it. Run upload script first
```
docker-compose build
docker-compose up -d   
./init.sh
docker-compose down
```
It will take about 3-4 hours when all data will be available in folder ./data

### Infrastructure
To get NARCIS infrastructure up and running execute commands
```
docker-compose build
docker-compose up  
```
The infrastructure consists of the following components:
##### MongoDB container (mongonarcis)
##### Elasticsearch (elasticsnarcis)
##### Jupyter notebook (jupyter)
##### Flask app (web)
Please note that Jupyter notebook is running on port 8880. To access it go to 0.0.0.0:8880 and copy/paste the token shown as result of "docker-compose up" command.
