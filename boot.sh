#!/bin/bash
# this script is used to boot a Docker container
source venv/bin/activate
flask db upgrade
flask translate compile
exec pyagent run -c /etc/appdynamics.cfg -- gunicorn -b :5000 --access-logfile - --error-logfile - microblog:app
