FROM zeromqorg/malamute
RUN sudo apt-get install -y python3-pip
COPY requirements.txt /tmp/requirements.txt
RUN sudo pip3 install -r /tmp/requirements.txt
RUN sudo mkdir -p /opt/sandbox
RUN sudo chown zmq:zmq /opt/sandbox
WORKDIR /opt/sandbox
ENV PYTHONPATH=/home/zmq/czmq/bindings/python:/home/zmq/malamute/bindings/python
