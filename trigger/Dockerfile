FROM zeromqorg/malamute
RUN sudo apt-get install -y python3-pip
COPY requirements.txt /tmp/requirements.txt
RUN sudo pip3 install -r /tmp/requirements.txt
RUN sudo mkdir -p /opt/sandbox
RUN sudo chown zmq:zmq /opt/sandbox
RUN sudo mkdir -p /home/zmq/.ssh
RUN sudo chown zmq:zmq /home/zmq/.ssh
RUN ssh-keyscan -t rsa github.com >> /home/zmq/.ssh/known_hosts
WORKDIR /opt/sandbox
ENV PYTHONPATH=/home/zmq/czmq/bindings/python:/home/zmq/malamute/bindings/python
