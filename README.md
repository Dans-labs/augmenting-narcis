# augmenting-narcis
## Assessment for NARCIS Publication Information Enrichment
To get NARCIS infrastructure up and running execute commands
```
docker-compose build
docker-compose up 
```
### Infrastructure
The infrastructure consists of the following components:
##### MongoDB container (mongonarcis) 
##### Elasticsearch (elasticsnarcis) 
##### Jupyter notebook (jupyter)
##### Flask app (web)
Please note that Jupyter notebook is running on port 8880. To access it go to 0.0.0.0:8880 and copy/paste the token shown as result of "docker-compose up" command. 
