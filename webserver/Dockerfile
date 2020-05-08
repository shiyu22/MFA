From conda/miniconda3-centos7

WORKDIR /app
COPY . /app

RUN yum -y update
RUN pip install -r /app/requirements.txt

RUN mkdir -p /tmp/import-pic

RUN cd /app
CMD python src/app.py