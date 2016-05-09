Purpose
=======

This little todo webapplication is strongly based on the bottle tutorial but uses Jinja2
templates instead of the standard SimpleTemplates. I've created this little project for
a talk about application development at the PythonTrier Meetup. The talk covered some basic
aspects like

* virtual environments
* clean code (pep8, pylint)
* testing (pytest)
* test coverage (coverage)

Installation
============

Clone this repository, create and activate a new virtual environment (python 3.5x is strongly recommended) and install
the dependencies:

    pip install -r requirements.txt

Then, create the initial database (todo.db in the current directory):

    python create_db.py

Start server
============

Start the server with

    python todo.py

It has three very simple REST views:

* http://localhost:8080/todo
* http://localhost:8080/new
* http://localhost:8080/edit/1

If you miss navigation or the D from CRUD: take the challenge and extend the application. And don't forget
linting and testing. You should fork the Github repo so that you have your own playground.
