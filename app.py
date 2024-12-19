from fastapi import FastAPI, Body
import requests
from pydantic import BaseModel
import redis
from datetime import datetime
import json
from uuid import UUID, uuid4

app = FastAPI()
client = redis.Redis(host='localhost', port=6379, decode_responses=True)

class DataModel(BaseModel):
    model_id: UUID
    scores: dict
    user_id: UUID
    timestamp: datetime
    score_id: UUID

@app.get("/")
def read_root():
    """
    Initialize API server and connects client to Redis server.

    Returns:
    dict: Initialization message.
    """
    return {"message": "Initialize redis cache."} 



@app.get("/model/{score_id}")
def read_item(score_id: str):
    """
    Get a Redis storage cache based on the specific score_id. 
    
    Parameters: 
    score_id (int): the score_id of the actual object

    Returns:
    dict: Simple score_id and regular id
    """
    try:
       client_data = client.get(score_id)
       client_data = json.loads(client_data)
       
       if client_data:
           return client_data
    except Exception as e:
        return {"message": str(e)}


@app.post('/model')
def post_item(model_id: str = Body(default=None), scores: dict = Body(default=None), user_id: str = Body(default=None), score_id: str = Body(default=None)):
    """
    Post data to Redis storage cache for the specific user_id. 
    
    Parameters:
    model_id (UUID): the model_id of the specific data model for the user
    scores (dict): dictionary containing the separate scores for data
    user_id (UUID): the id of the specific user for the model
    timestamp (datetime): the datetime object containing the time the entry was added
    score_id (UUID): the id of the specific entry
    
    Returns:
    bool: whether or not the data was successfully added
    """ 
    try:
        timestamp = datetime.now()
        check_exist = client.get(score_id) == None
        if check_exist:
            response = client.set(score_id, DataModel(model_id=model_id, scores=scores, user_id=user_id, timestamp=timestamp, score_id=score_id).model_dump_json())
            if response:
                return {"message": "Data successfully added to Redis", "score_id": score_id}
        return {"message": f"Specific score_id {score_id} already exists."}
    except Exception as e:
        return {"message": str(e)}