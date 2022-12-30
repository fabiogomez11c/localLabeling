import requests
import time
import pandas as pd

def request_test(x):
  url = 'https://us-east1-mom-seguros.cloudfunctions.net/classify_ic'
  body = {}

  now = time.time()
  x = requests.post(url, json = body)
  try:
    result = {**x.json()}
  except:
    result = {'prediction': 'error'}
  result['exec_time'] = round(time.time() - now, 2) 

  return result

result = list(map(request_test, list(range(1000))))
result = pd.DataFrame(result)

print(result.info())
result.to_csv('traffic_result.csv')





