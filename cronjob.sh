#! /bin/bash
cd <app_location>
PYTHON=$(which python)
PIP=$(which pip3)

if [ ! -d "./env"]
then
    ${PYTHON} -m venv env
fi

source env/bin/activate
${PIP} install -r requirements.txt
${PYTHON} cloudflare.py

deactivate
