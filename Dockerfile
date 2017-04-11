FROM bvlc/caffe:cpu 

ADD src /workspace

RUN pip install -r /workspace/requirements.txt

EXPOSE 5000
