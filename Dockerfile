FROM bvlc/caffe:cpu 

EXPOSE 5000

RUN apt-get install -y --no-install-recommends graphviz python-dev python-pil python-pip 

VOLUME /data
EXPOSE 5000

RUN mkdir /workdir

ADD src /workdir

RUN pip install -r /workdir/requirements.txt 

RUN python /workdir/app.py