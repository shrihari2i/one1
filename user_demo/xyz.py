import requests
import json
 
URL = "http://43.205.44.117:8000"
 
data = {
    "day_score":1,
    "number_of_days_participated":2,
   
}
 
json_data = json.dumps(data)
r = requests.post(url = URL, data = json_data)
data = r.json
