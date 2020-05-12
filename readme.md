# Simple-Celery

Simple-Celery is a simple python application that utilises celery.

## First Time Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the dependencies.

```bash
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## Usage

```bash
source venv/bin/activate
celery -A core worker --loglevel=info
```