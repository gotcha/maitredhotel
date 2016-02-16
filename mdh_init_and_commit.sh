#!/bin/bash

set -ex

DEST=/opt/sandbox/mdhtest
ls -al  ~
ls -al  ~/.ssh
cat ~/.ssh/known_hosts
python3 /opt/mdh.py init \
   --git-email=mdh@bubblenet.be  --git-name="Maitre d'hotel" \
   "$2" "${DEST}"
python3 /opt/mdh.py commit --name="$1" tcp://malamute:9999 "${DEST}"
