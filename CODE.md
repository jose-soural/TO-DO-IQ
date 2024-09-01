# The code of TO-DO-IQ

The code of TO-DO-IQ is based only on pythons default modules, meaning no extra installation is required.

It is naturally divided into three, largely indepent layers + a setup procedure, each with its own dedicated .py file:

## dltl.py

The base of the whole task management system, this file sets up the DLTL (Doubly linked task list) and related classes and some of their methods. The inner workings of these classes and methods should be largely clear from the code itself and the provided docstrings.

It is purposefully designed to not depend on the end implementation of the later two layers as much as possible, meaning it could be reused for a similiar project following a different implementation methodology.

## functions.py

The body of the app. Houses the main functionality of the programme, takes care of the actual task managing. The inner workings the included functions and methods should be largely clear from the code itself and the provided docstrings.

The user cannot interact with this layer directly.

## main.py

The face of the programme. Through the use of argparse it handles receiving user input, preprocessing it and passing it to functions.py.

## setup.py

A module for setting up your own instance of TO-DO-IQ.

In reality, all it does is reset the state of the directory and returns functions.py to the "factory" settings.
