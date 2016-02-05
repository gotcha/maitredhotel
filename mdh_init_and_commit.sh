#!/bin/bash

set -ex

DEST=/home/zmq/mdhtest
python3 /opt/mdh.py init \
   --git-email=mdh@bubblenet.be  --git-name="Maitre d'hotel" \
   git@github.com:gotcha/mdhtest.git "${DEST}"
python3 /opt/mdh.py commit tcp://malamute:9999 "${DEST}"
