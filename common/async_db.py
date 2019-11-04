from motor.motor_asyncio import AsyncIOMotorClient


def get_mongo_db(uri, db):
    client = AsyncIOMotorClient(uri)
    db = client[db]
    return db
