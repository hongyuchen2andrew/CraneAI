#!/bin/bash

if [ "$1" == "dev" ]; then
    export FLASK_APP=webapp
    export FLASK_ENV=development
    export FLASK_DEBUG=1
    flask run --port=5001
elif [ "$1" == "prod" ]; then
    gunicorn webapp.wsgi:app
else
    echo "Invalid argument. Please use 'dev' or 'prod'."
fi