#! /bin/bash

PYTHON=$(which python3)
PIP=$(which pip3)

cd /root/scripts/cloudflare-ddns

if [ ! -d "./env" ]
then
    ${PYTHON} -m venv env
fi

source env/bin/activate

sleep 1
${PIP} install -r requirements.txt
sleep 1
${PYTHON} cloudflare.py

deactivate
