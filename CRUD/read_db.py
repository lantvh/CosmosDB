from fastapi import FastAPI, HTTPException
from pymongo import MongoClient

app = FastAPI()

# Xác thực bằng Python connection string của Azure CosmosDB for MongoDB
client = MongoClient(
    "mongodb://lantvh-mongo:ep2J3qzvMRJYuhrVVxFC6aN8UfCDKswpQqdgehAiID06rSexdZvPpu21QlPSN5uzGwk4SviV4To6ACDbAn60mw==@lantvh-mongo.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@lantvh-mongo@")

@app.get("/{database}/{collection}")
def get_all_documents(database: str, collection: str):
    # Kiểm tra nếu database không tồn tại
    if database not in client.list_database_names():
        raise HTTPException(status_code=404, detail={"error": "Database not found"})
    # Kiểm tra nếu collection không tồn tại trong database
    if collection not in client[database].list_collection_names():
        raise HTTPException(status_code=404, detail={"error": "Collection not found"})

    # Query tất cả các documents trong collection trong database
    db = client[database]
    collection = db[collection]
    results = collection.find({})
    documents = [str(doc) for doc in results]
    return {"data": documents}