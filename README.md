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

# Configure Full Text Search (Currently Deprecated)

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

Alter user role:

```bash
[sudo -u postgres] psql -c "ALTER ROLE wisecity superuser;"
```

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

** Restart your postgres. **

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

When constructing front-end modules, make sure you are in `front-end` directory, and run `npm run dev` to compile Javascript files in real-time.

Before deploying to the server, make sure you've run command `npm run build` to minimize the scripts.

To add a new front-end library, install it, edit file `front-end/js/vendor.js`, and then run `npm run `npm run vendor`.

## Folders

 + `front-end/dest/`: Temporary files while developing.
 + `front-end/build/`: Built files for deployment.
 + `front-end/js/`: Javascript / Vue.js source file.
 + `front-end/vendor/`: Third-party libaries.
 + `front-end/styles/`: Custom style files (SCSS Language).
 + `templates/`: Template files for Django (Jinja2 Language).