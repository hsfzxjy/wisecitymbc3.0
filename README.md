# wisecitymbc3.0
Website for wisecitymbc 3.0. Brighter &amp; better.

# Requirements

 + Python >= 3.5.1
 + Postgresql >= 9.4 (username: wisecity, password: 12345. Only for test)

## Configuration for Postgresql

```bash
$ [sudo -u postgres] createuser --pwprompt wisecity
$ [sudo -u postgres] createdb -Owisecity -Eutf8 app_wisecitymbc
```

Test:

```bash
$ [sudo -u postgres] psql app_wisecitymbc
```

# Configure Full Text Search (NEW)

## Installation

```bash
# Install SCWS
wget http://www.xunsearch.com/scws/down/scws-1.2.2.tar.bz2
tar xvf scws-1.2.2.tar.bz2
cd scws-1.2.2
./configure
sudo make install

# Install postgresql-server-dev
# NOTICE: Use your own postgres version. Mine is 9.4
sudo apt-get install postgresql-server-dev-9.4

# Install zhparser
git clone https://github.com/amutu/zhparser.git
SCWS_HOME=/usr/local make
sudo make install
```

## Configure

Checkout your config file location:

```bash
[sudo -u postgres] psql -c "show config_file"
```

Append the following lines to `<config file>`:

```
zhparser.multi_short = t
zhparser.dict_in_memory = t
zhparser.punctuation_ignore = t
```

Run initial operations:

```bash
./manage.py installdb
```

# Installation

Install python virtual environment:

```bash
pyvenv .env
source .env/bin/activate
```

Install required python packages:

```bash
pip install -r requirements.txt
```

Install npm dependencies:

```bash
cd front-end && npm install
```

# Development for front-end

While constructing frontend modules, you should run `cd front-end/ && webpack --watch` and `./manage.py runserver` first, and keep them running.

## Folders

 + `front-end/dest/`: contains compiled bundles included by the pages.
 + `front-end/entries/`: should ONLY contain entry scripts which will be compiled into bundles.
 + `front-end/components/`: should contain vue components.
 + `templates/`: contains template files for Django.

Checkout [branch test-webpack](https://github.com/hsfzxjy/wisecitymbc3.0/tree/test-webpack) for a detailed example.