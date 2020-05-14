From python:3.7.7

WORKDIR /app
COPY . /app

RUN apt-get -y update
RUN apt-get -y install libsndfile1
RUN pip install -r /app/requirements.txt

RUN mkdir -p /tmp/import-pic
RUN mkdir -p /tmp/data-pic

RUN cd /app
CMD python src/app.py