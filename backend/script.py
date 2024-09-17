import pymongo
import json
import os

from dotenv import load_dotenv

load_dotenv()

client = pymongo.MongoClient(os.environ.get('MONGO_DB_SERVICE'))

db = client['courses_db']
collection = db['courses']

collection.create_index('name')

with open("courses.json", "r") as file:
    courses = json.load(file)

try:
    if courses:
        for course in courses:
            course['rating'] = {'total': 0, 'count': 0}

            for chapters in course['chapters']:
                course['rating'] = {'total': 0, 'count': 0}

            collection.insert_one(course)

    print("DATA MIGRATED SUCCESSFULLY")
except Exception as exc:
    print("ERROR:  ", exc)

client.close()
