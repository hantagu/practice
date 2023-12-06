from database import DBHelper

import jwt
from dotenv import dotenv_values
from flask import Flask, Response, make_response, redirect, render_template, request, url_for

PAGE_MAIN = 'main'

PAGE_USERS = 'users'
PAGE_GROUPS = 'groups'
PAGE_COURSES = 'courses'

PAGE_TASKS_INFO = 'tasks-info'
PAGE_GROUPS_INFO = 'groups-info'
PAGE_GROUP_INFO = 'group-update'
PAGE_COURSE_INFO = 'course-update'


app = Flask(__name__)
config = dotenv_values('.env')
app.secret_key = config['APP_SECRET']
db = DBHelper(config['POSTGRES_HOST'], config['POSTGRES_PORT'], config['POSTGRES_USER'], config['POSTGRES_PASSWD'], config['POSTGRES_DBNAME']) # type: ignore


def template(page: str, **kwargs) -> Response:
    resp = make_response(render_template(f'{page}.html', page=page, **kwargs))
    return resp


@app.get('/test')
def test():
    return str()


@app.get('/')
def index():
    return template(PAGE_MAIN)


@app.get(f'/{PAGE_USERS}')
def users():
    return template(PAGE_USERS, users=db.get_all_users())


@app.get(f'/{PAGE_GROUPS}')
def groups():
    return template(PAGE_GROUPS, groups=db.get_all_groups())


@app.get(f'/{PAGE_COURSES}')
def courses():
    return template(PAGE_COURSES)


app.run(host=config['APP_ADDR'], port=config['APP_PORT']) # type: ignore
