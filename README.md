# Python Chess AI

## Overview
This is a fun project to learn a bit more about python chess AIs. Right now the plan is to play around with evaluation functions and minimax to see how good of an AI I can get for solving tactics. Short term goal is to get it setup to play games with user input, long term goal to plug into the lichess api.

## Requirements
Python 3.8+ 

See `requirements.txt`

## Building and Running
Right now there is a `makefile` at the top level that can work with ubuntu.

`make setup`  : will get the virtual environment setup and install the requirements needed.

`make test` : runs the test cases that exist

`make lint` : runs black to keep the code nice and clean

There will soon be an interface for playing a game, but first focus is improving the evaluation to be able to handle lots of tactical situations and then gameplay!