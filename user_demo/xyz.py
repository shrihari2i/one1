import requests
import json
 
URL = "http://127.0.0.1:8000/score/"
 
data = {
    "day_score":1,
    "number_of_days_participated":2,
   
}
 
json_data = json.dumps(data)
r = requests.post(url = URL, data = json_data)
data = r.json