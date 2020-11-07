# minesCrowdsourcing

![Django CI](https://github.com/leochely/minesCrowdsourcing/workflows/Django%20CI/badge.svg)
[![codecov](https://codecov.io/gh/leochely/minesCrowdsourcing/branch/master/graph/badge.svg?token=z5oskcnnLS)](https://codecov.io/gh/leochely/minesCrowdsourcing)

A Crowdsourcing Web Application for Supporting Research at Mines and the Beyond


## Getting started

### Virtual Environment
If you want to use a virtual environment, make sure you have `virtualenv` installed and run the following command.
```bash
virtualenv .venv
```
To activate your virtual environment, run `source .venv/bin/activate` (Mac/Linux) or `source .venv/Scripts/activate` (Windows).

### Installing Requirements
Run 
```bash
pip install -r requirements.txt
```

### Running a Local Instance
For the first time, you need to initialize the database by running the migrations. You can then run a localserver that you can access at http://127.0.0.1:8000/ by default. You can find more options for this command [here](https://docs.djangoproject.com/en/3.0/ref/django-admin/#runserver).
```bash
python3 manage.py migrate
python3 manage.py runserver 
```
