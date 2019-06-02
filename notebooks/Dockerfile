FROM jupyter/datascience-notebook
COPY ./ /home/jovyan/work
WORKDIR /home/jovyan
#RUN apt-get update
#RUN apt-get -y install vim
RUN pip install -r requirements.txt
