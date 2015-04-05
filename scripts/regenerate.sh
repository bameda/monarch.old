#!/bin/bash

# For postgresql
echo "-> Remove monarch DB"
dropdb monarch
echo "-> Create monarch DB"
createdb monarch
echo "-> Create DB tables"
python manage.py migrate

#echo "-> Generate sample data"
#python manage.py sampledata --traceback
