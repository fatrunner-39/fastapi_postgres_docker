#!/bin/bash

echo "create database"
set -e

psql -U $POSTGRES_USER -h db -p 5432 -c "CREATE DATABASE $POSTGRES_NAME"
