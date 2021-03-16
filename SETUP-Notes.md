# Server Setup:

Reference:
- https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-14-04
- http://www.markjberger.com/flask-with-virtualenv-uwsgi-nginx/

## Install Packages:
```shell
apt-get install -y build-essential python3 python3-dev python3-pip \
nginx uwsgi uwsgi-plugin-python unzip libaio-dev
sudo pip install virtualenv

mkdir ~/webapi
cd ~/webapi
```

## Install Oracle Instantclient and cx_Oracle
__Reference__: https://help.ubuntu.com/community/Oracle%20Instant%20Client  
__Reference__: https://gist.github.com/kimus/10012910  

## Setup Virtualenv and Flask
```shell
virtualenv venv --no-site-packages
source venv/bin/activate
pip3 install flask

deactivate
```

## Setup uWSGI
```shell
touch ~/webapi/webapi.sock
sudo chown <USER>:www-data webapi.sock
```
__webapi.ini has to be in ~/webapi__

## Setup Nginx
- Remove 'default' files from /etc/nginx/sites-available
- Copy webapi.nginx config file to /etc/nginx/sites-available
- Create a link to enable it:
```shell
sudo ln -s /etc/nginx/sites-available/webapi /etc/nginx/sites-enabled
```

## Flask Server Startup Process:
- Nginx runs /etc/nginx/sites-enabled/webapi on port 80
- webapi site starts uWSGI using ~/webapi.ini
- uWSGI runs webapi.py and creates a socket; ~/webapi/webapi.sock
- webapi.py imports config.py for database credentials
- Oracle Instantclient variables have to be setup in ~/.bashrc
