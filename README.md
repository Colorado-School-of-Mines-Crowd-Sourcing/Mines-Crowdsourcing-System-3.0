# minesCrowdsourcing

A Crowdsourcing Web Application for Supporting Research at Mines and the Beyond


## Getting started
Installing and running MCS locally is fairly straightforward. This tutorial assumes that python3, pip, virtualenv, and docker are installed and the docker daemon is running. First, clone the git repository and change it to the current directory. Now, the requirements have to be installed in a virtual environment.
### Virtual Environment
```bash
cd minesCrowdsourcing
virtualenv .venv
source .venv/bin/activate
```
If on Windows run the following instead.
```bash
source .venv/Scripts/activate
```


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

## Running MCS in a Docker Container
After completing the getting started section, MCS can be started in a Docker container. First a self-signed certificate must be created. 
```bash
openssl req -newkey rsa:2048 -nodes -keyout self-signed-certs/mcs.key -x509 -days 365 -out self-signed-certs/mcs.crt
```
Then the container can be built.
```bash
docker build -t mines-crowdsourcing-app .
```
Then the container can be started on port 9601 to access the website at https://0.0.0.0:9601. It also requires port 9600 for gunicorn to run. You will likely have to circumvent your browser's security protections to view the website. You can also configure your OS to accept your self-signed certificate.
```bash
docker run -it -p 9601:9601 mines-crowdsourcing-app
```
## Email
Emails are set up to be sent out when a user completes a task or their balance changes. To activate this feature modify the email section of minesCrowdsourcing/settings.py and remove the comments on the email functions. 



