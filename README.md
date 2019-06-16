# Restaurant App - FrauenLoop

Building an API using Python, Flask.

## SETUP

I assume you already installed Python 3.4 or higher and pip.

### Virtual Environment

Install virtualenv via pip:

```
$ pip3 install virtualenv
```

Create a virtual environment for a project:

```
$ cd restaurant-app
$ python3 -m venv myvenv
```

To begin using the virtual environment, it needs to be activated:

```
$ source myvenv/bin/activate
```

Install Flask:

```
(venv) $ pip3 install flask
```

### Run server

With this command:

```
(venv) $ export FLASK_APP=run.py
(venv) $ export PYTHONPATH=/Path/to/the/app
(venv) $ flask run
```

### In Browser

Paste this url and hit enter:

```
http://localhost:5000/
```

### Tests

You can run the tests with this command:

```
(venv) $ python3 project/test_views.py
```

