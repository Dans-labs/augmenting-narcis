# augmenting-narcis
## Assessment for NARCIS Publication Information Enrichment
### Downloads
Download NARCIS data from https://dataverse.nl/dataset.xhtml?persistentId=hdl:10411/8H4QSU in the current folder (augmenting-narcis)

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
