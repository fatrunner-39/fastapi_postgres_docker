#!/bin/bash

sleep 3

echo "create migrations"
alembic upgrade head


echo "start application"
python3 main.py