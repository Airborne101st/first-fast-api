import os

from motor.motor_asyncio import AsyncIOMotorClient


client = AsyncIOMotorClient(os.environ.get('MONGO_DB_SERVICE'))
db = client['courses_db']
users_collection = db['users']

