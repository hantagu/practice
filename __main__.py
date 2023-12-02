from database import DBHelper

from dotenv import dotenv_values
from flask import Flask, redirect, url_for, render_template


PAGE_USERS = 'users'
PAGE_GROUPS = 'groups'
PAGE_COURSES = 'courses'

PAGE_TASKS_INFO = 'tasks-info'
PAGE_GROUPS_INFO = 'groups-info'
PAGE_GROUP_INFO = 'group-update'
PAGE_COURSE_INFO = 'course-update'


app = Flask(__name__)
config = dotenv_values('.env')
db = DBHelper(config['POSTGRES_HOST'], config['POSTGRES_PORT'], config['POSTGRES_USER'], config['POSTGRES_PASSWD'], config['POSTGRES_DBNAME']) # type: ignore


@app.get('/')
def index():
    return '*auth*'


@app.get(f'/{PAGE_USERS}')
def users():
    return PAGE_USERS


@app.get(f'/{PAGE_GROUPS}')
def groups():
    return PAGE_GROUPS


@app.get(f'/{PAGE_COURSES}')
def courses():
    return PAGE_COURSES


app.run(host='localhost', port=8080)
