# TWEPY
##Twitter & Elasticsearch in Python
Twitter & Elasticsearch interface in Python


## How to Use

### Create virtualenv
Create and run Python3 Virtualenv:
```
$ python virtualenv .venv
$ source .venv/bin/activate
$ make deps
```

Obs: if your distro uses Python 2 by default, you can user virtualenv parameter `-p python3` for create Python3 Virtualenv


### Create your Twitter App

- Access and login in this URL https://apps.twitter.com/
- Use `Create New App`
- After creating, acess `Keys and Access Tokens`, its is need for create process


### Preparing to use

- In terminal use command `$ make config`
- In terminal run `$ make auth` and follow your instructions
- Edit your `app/config.py` using your Elasticsearch and Twitter informations


### Let's talk about Docker

- If you want, you can use this app with docker
- After install `docker` and `docker-compose`, run `$ make up` for start compose
- You can stopping compose using `$ make stop`


### Run the app

- run `$ make stream` and enjoy.
