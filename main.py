import contextlib
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from pymongo import MongoClient
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from pydantic import BaseModel
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from database import users_collection
from utils import hash_password, verify_password
from auth import create_access_token

app = FastAPI()

load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get('FRONTEND_SERVICE')],  # Add your frontend origin here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient(os.environ.get('MONGO_DB_SERVICE'))
db = client['courses_db']

print("SERVICE", os.environ.get('FRONTEND_SERVICE'))
print("START")

class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


@app.post('/register')
async def register(user: UserRegister):
    existing_user = await users_collection.find_one({'username': user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail='Username already taken')

    hashed_password = hash_password(user.password)
    user_data = {
        'username': user.username,
        'email': user.email,
        'password': hashed_password
    }
    await users_collection.insert_one(user_data)
    return {'msg': 'User created successfully!'}


@app.post('/login')
async def login(user: UserLogin):
    db_user = await users_collection.find_one({'username': user.username})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail='Invalid Credentials!')

    access_token = create_access_token(data={'sub': user.username})
    return {'token': access_token, 'token_type': 'bearer'}


@app.get('/courses/')
def get_courses(sort_by: str = 'date', domain: str = None):
    course_list = []
    for course in db.courses.find():
        total = 0
        count = 0
        for chapter in course.get('chapters', []):
            ratings = chapter.get('ratings', {})
            total += ratings.get('total', 0)
            count += ratings.get('count', 0)

        db.courses.update_one(
            {'_id': course['_id']},
            {'$set': {'rating': {'total': total, 'count': count}}}
        )

    sort_options = {
        'date': ('date', -1),
        'rating': ('rating', -1),
        'alphabetical': ('alphabetical', 1)
    }
    sort_field, sort_order = sort_options.get(sort_by, ('date', -1))

    query = {}
    if domain:
        query['domain'] = domain

    courses = db.courses.find(query, {'name': 1, 'date': 1, 'description': 1, 'domain': 1, 'rating': 1, '_id': 1}).sort(
        sort_field, sort_order)
    for course in courses:
        course['_id'] = str(course['_id'])
        course['date'] = datetime.fromtimestamp(course['date']).strftime('%Y-%m-%d')
        course_list.append(course)
    return course_list


@app.get('/courses/{course_id}')
def get_course(course_id: str):
    course = db.courses.find_one({'_id': ObjectId(course_id)},
                                 {'name': 1, 'domain': 1, 'description': 1, 'date': 1, 'chapters': 1, '_id': 0})
    course['date'] = datetime.fromtimestamp(course['date']).strftime('%Y-%m-%d')
    if not course:
        raise HTTPException(status_code=404, detail='Course not found')
    try:
        course['rating']['total']
    except KeyError:
        course['rating'] = 'Not rated yet'
    return course


@app.get('/courses/{course_id}/{chapter_id}')
def get_chapter(course_id: str, chapter_id: int):
    course = db.courses.find_one({'_id': ObjectId(course_id)}, {'_id': 0})
    if not course:
        raise HTTPException(status_code=404, detail='Course not found')
    chapters = course.get('chapters', [])
    try:
        chapter = chapters[chapter_id]
    except (ValueError, IndexError) as e:
        raise HTTPException(status_code=404, detail='Chapter not found') from e
    return chapter


@app.post('/courses/{course_id}')
def rate_course(course_id: str, rating: int = Query(..., gt=-2, lt=2)):
    course = db.courses.find_one({'_id': ObjectId(course_id)}, {'_id': 0})
    if not course:
        raise HTTPException(status_code=404, detail='Course not found')
    try:
        course['rating']['total'] += rating
        course['rating']['count'] += 1
    except KeyError:
        course['rating'] = {'total': rating, 'count': 1}
    db.courses.update_one({'_id': ObjectId(course_id)}, {'$set': {'rating': rating}})
    return course


@app.post('/courses/{course_id}/{chapter_id}')
def rate_chapter(course_id: str, chapter_id: int, rating: int = Query(..., gt=-2, lt=2)):
    course = db.courses.find_one({'_id': ObjectId(course_id)}, {'_id': 0})
    if not course:
        raise HTTPException(status_code=404, detail='Course not found')
    chapters = course.get('chapters', [])
    try:
        chapter = chapters[chapter_id]
    except (ValueError, IndexError) as e:
        raise HTTPException(status_code=404, detail='Chapter not found') from e
    try:
        chapter['rating']['total'] += rating
        chapter['rating']['count'] += 1
    except KeyError:
        chapter['rating'] = {'total': rating, 'count': 1}

    db.courses.update_one({'_id': ObjectId(course_id)}, {'$set': {'chapters': chapters}})
    return chapter
