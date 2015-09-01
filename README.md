# TWEPY
##Twitter & Elasticsearch in Python
Twitter & Elasticsearch interface in Python


## How to Use

### Create virtualenv
Create and run Python3 Virtualenv:
```
$ python virtualenv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

Obs: if your distro uses Python 2 by default, you can user virtualenv parameter `-p python3` for create Python3 Virtualenv


### Create your Twitter App

- Access and login in this URL https://apps.twitter.com/
- Use `Create New App`
- After creating, acess `Keys and Access Tokens`, its is need for create process

### Changing the config.py

- In terminal use command `$ cp config.py.example config.py`
- In terminal run `$ python twitter-authorize.py` and follow your instructions
- Edit your `config.py` using your Elasticsearch and Twitter informations

### Run the script and fun!!
