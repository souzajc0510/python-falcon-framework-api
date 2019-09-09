#!/bin/bash

pip install --upgrade pip
pip install -r /app/requirements.txt

/usr/local/bin/python3 /app/services/create_schema_service.py

gunicorn app:api -c /app/conf/gunicorn_conf.py --reload