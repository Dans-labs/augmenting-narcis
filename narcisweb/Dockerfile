FROM python:3.6
MAINTAINER Vyacheslav Tykhonov
COPY . /narcis
WORKDIR /narcis
RUN apt-get update
RUN apt-get -y install vim 
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
