# Project

Flask Blog website

## Languages

[![made-with-python](https://img.shields.io/badge/Made%20with-Flask-1f425f.svg)](https://www.python.org/)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

## Description
This is a compact blogging platform where users can create, update, like, dislike, and comment on posts. The primary objective behind developing this project is to grasp the intricacies of establishing connections with multiple databases and effectively utilizing them. Additionally, it serves as a valuable tool for revisiting and reinforcing learned concepts.

## Installation
- Use the package manager [pip](https://pip.pypa.io/en/stable/) to install below packages.
```bash
create a venv
windows: python -m venv ./venv
Linux: python -m venv venv

Make sure to be in root directory
```
- Step install packages manullay or from requirements.txt
```bash
pip install flask Flask-SQLAlchemy flask-cors Flask-Migrate flask-redis flask-marshmallow

```
- Install from the requirements file
```bash
pip install -r requirements.txt
```
- Create .env file in root directory and set the below variables in it
```env
# env variables

SECRET_KEY = 
JWT_SECRET_KEY = 

db1_user=
db1_password=
db1_port=
db1_host=
db1_dbname=

db2_user=
db2_password=
db2_port=
db2_host=
db2_dbname=

environment = dev
Make sure to name this variable with file name we goinng to created below In my case it's dev
```
- Create a **.py** file in the [config](backend/config) directory, you can name it dev.py, prod.py or qa.py as per you environment
    - You can make connection to any database and set it according to you'r requirements
    - This is just a sample file.
    - ``` SQLALCHEMY_BINDS = { "pg_sql1": f"postgresql://url } ``` if you change **"pg_sql1"** in this make sure to change ** __bind_key__** in [models.py](backend/app/api/models/models.py)

```python

import os
from datetime import timedelta
from urllib.parse import quote

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")

SQLALCHEMY_DATABASE_URI = f"postgresql://{os.environ.get('db1_user')}:{quote(os.environ.get('db1_password'))}@{os.environ.get('db1_host')}:{os.environ.get('db1_port')}/{os.environ.get('db1_dbname')}"

SQLALCHEMY_BINDS = {
    "pg_sql1": f"postgresql://{os.environ.get('db2_user')}:{quote(os.environ.get('db2_password'))}@{os.environ.get('db2_host')}:{os.environ.get('db2_port')}/{os.environ.get('db2_dbname')}" # noqa
}

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

JWT_COOKIE_SECURE = False

JWT_TOKEN_LOCATION = ["cookies"]

JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
```

## Create tables in the database
- After completion of above task navigate to ```backend ``` directory and run create-db command.
```bash
cd backend
flask create-db
```

## How to run
- Go to ```cd backend```
- Execute ```python run.py ``` to run it on local

**Note:** On production always use production WSGI 

## Api endpoints

> Auth API

    Method: POST
    Endpoint: /api/v1/auth/register/
    Payload: {"username": "username", "password": "password 8 char long" }
    --------------------------------------------------------------------------------------
    Method: POST
    Endpoint: /api/v1/auth/login/
    Payload: {"username": "username", "password": "password"}
    --------------------------------------------------------------------------------------
    Method: POST
    Endpoint: /api/v1/auth/logout/

> Post API

    Method: GET
    Endpoint: /api/v1/post/
    --------------------------------------------------------------------------------------
    Method: POST
    Endpoint: /api/v1/post/
    Payload: {"post_content": "you post content" }
    --------------------------------------------------------------------------------------
    Method: PACTH
    Endpoint: /api/v1/post/
    Payload: {"post_content": "you post content", "post_id": post id to update }

> Comment API

    Method: POST
    Endpoint: /api/v1/comment/
    Payload: {"post_id": Id of the post, "comment": "Comment to make" }
    --------------------------------------------------------------------------------------
    Method: PATCH
    Endpoint: /api/v1/comment/
    Payload: {"comment_id": Id of the comment, "comment": "Comment to make" }
    --------------------------------------------------------------------------------------
    Method: DELETE
    Endpoint: /api/v1/comment/delete/<int:comment_id>

> Like Dislike API

    Method: POST
    Endpoint: /api/v1/postlike/
    Payload: {"post_id": Id of the post to like or dislike}

## The main file of the code is below
The Refrence for the main file of the program is [__init__ File](app/__init__.py)

