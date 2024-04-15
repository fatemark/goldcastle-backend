#!/bin/bash

# Script 1
gunicorn --bind 0.0.0.0:4000 app.ServerRequests:app &

cd scripts/discord

python3 johnny.py &

# Script 3
python3 rosy.py &

python3 galacticcat.py &

curl https://goldcastle.club/api/checkingDatabase &

wait