import requests

def request_test():
  url = 'https://us-east1-mom-seguros.cloudfunctions.net/classify_ic'
  body = {}

  x = requests.post(url, json = body)

  return x.text









