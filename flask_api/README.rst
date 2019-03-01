install:
run "pip3 install -e . --user" in flask_api directory

running:
run api.py
use postman(https://www.getpostman.com/) to hit api

deploy:
$ cd path/to/flask_api_directory/
$ virtualenv env
$ source env/bin/activate
$ pip install -e .
$ zappa deploy dev

database:
get a connection and a cursor
use the cursor to execute sql commands
fetch the results with fetchall() or fetchone()

credentials:
to hit database or deploy requires a credentials file in a .aws directory in your home directory with chmod 600 permissions