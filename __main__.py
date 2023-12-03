from database import DBHelper

from dotenv import dotenv_values
from flask import Flask, Response, make_response, render_template


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
db = DBHelper(config['POSTGRES_HOST'], config['POSTGRES_PORT'], config['POSTGRES_USER'], config['POSTGRES_PASSWD'], config['POSTGRES_DBNAME'], False) # type: ignore


def template(page: str, **kwargs) -> Response:
    resp = make_response(render_template(f'{page}.html', page=page, **kwargs))
    return resp


@app.get('/')
def index():
    return '*auth*'


@app.get(f'/{PAGE_USERS}')
def users():
    return template(PAGE_USERS, users=db.get_all_users())


@app.get(f'/{PAGE_GROUPS}')
def groups():
    return template(PAGE_GROUPS)


@app.get(f'/{PAGE_COURSES}')
def courses():
    return template(PAGE_COURSES)


app.run(host=config['APP_ADDR'], port=config['APP_PORT']) # type: ignore
