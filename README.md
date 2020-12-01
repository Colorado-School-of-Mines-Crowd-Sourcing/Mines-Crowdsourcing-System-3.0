# minesCrowdsourcing

![Django CI](https://github.com/leochely/minesCrowdsourcing/workflows/Django%20CI/badge.svg)
[![codecov](https://codecov.io/gh/leochely/minesCrowdsourcing/branch/master/graph/badge.svg?token=z5oskcnnLS)](https://codecov.io/gh/leochely/minesCrowdsourcing)

A Crowdsourcing Web Application for Supporting Research at Mines and the Beyond


## Getting started
Installing and running MCS locally is fairly straightforward. This tutorial assumes that python3, pip, virtualenv, and docker are installed and the docker daemon is running. First, clone the git repository and change it to the current directory. Now, the requirements have to be installed in a virtual environment.
### Virtual Environment
```bash
cd minesCrowdsourcing
virtualenv .venv
source .venv/bin/activate
```
If on Windows run 
```bash
source .venv/Scripts/activate
```
instead.


### Installing Requirements
Run 
```bash
pip install -r requirements.txt
```

### Running a Local Instance
For the first time, you need to initialize the database by running the migrations and create a super user. You can then run a localserver that you can access at http://127.0.0.1:8000/ by default. You can find more options for this command [here](https://docs.djangoproject.com/en/3.0/ref/django-admin/#runserver).
```bash
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver 
```

## Building and Running Docker Container
First the container must be built.
```bash
docker build -t mines-crowdsourcing-app .
```
Then the container can be started on port 443 to access the website at https://minescrowdsourcingsystem.com:443.
```bash
docker run -it -p 443:443 mines-crowdsourcing-app
```



