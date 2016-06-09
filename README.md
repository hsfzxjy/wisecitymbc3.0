# wisecitymbc3.0
Website for wisecitymbc 3.0. Brighter &amp; better.

# Requirements

 + Python >= 3.5.1
 + Postgresql >= 9.3 (username: wisecity, password: 12345. Only for test)

## Configuration for Postgresql

```bash
$ [sudo -u postgres] createuser --pwprompt wisecity
$ [sudo -u postgres] createdb -Owisecity -Eutf8 app_wisecitymbc
```

Test:

```bash
$ [sudo -u postgres] psql app_wisecitymbc
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