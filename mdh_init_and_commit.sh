#!/bin/bash

set -ex

DEST=/opt/sandbox/mdhtest
python3 /opt/mdh.py init \
   --git-email=mdh@bubblenet.be  --git-name="Maitre d'hotel" \
   "$2" "${DEST}"
python3 /opt/mdh.py commit --name="$1" tcp://malamute:9999 "${DEST}"
