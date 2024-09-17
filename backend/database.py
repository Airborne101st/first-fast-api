import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# Load Env Variables
load_dotenv()

print("MONG Service: ", os.environ.get('MONGO_DB_SERVICE'))
client = AsyncIOMotorClient(os.environ.get('MONGO_DB_SERVICE'))
print("ZE CLIENT IS: ", client)
db = client['courses_db']
print("ZE DB IST: ", db)
users_collection = db['users']

