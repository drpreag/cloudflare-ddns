#! /bin/bash

PYTHON=$(which python3)

cd /root/scripts/cloudflare-ddns

if [ ! -d "./env" ]
then
    ${PYTHON} -m venv env
fi

source env/bin/activate
pip install -r ./requirements.txt
python cloudflare.py

deactivate
