import requests
import json
import sys

username = sys.argv[1]
password = sys.argv[2]
org_id = sys.argv[3]
env_id = sys.argv[4]
art_id = sys.argv[5]
version = sys.argv[6]

def get_access_token(username, password):
  body = {"username": username, "password": password }
  response = requests.post('https://anypoint.mulesoft.com/accounts/login', data = body)
  return response.json()['access_token']

def create_api(org_id, env_id, version, art_id, access_token):
  url = "https://anypoint.mulesoft.com/apimanager/api/v1/organizations/" + org_id + "/environments/" + env_id + "/apis"
  headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + access_token
  }
  payload = json.dumps({
    "spec": {
      "groupId": org_id,
      "assetId": art_id,
      "version": version
    },
    "endpoint": {
      "uri": None,
      "proxyUri": None,
      "isCloudHub": True,
      "muleVersion4OrAbove": True
    },
    "instanceLabel": art_id
  })
  response = requests.request("POST", url, headers=headers, data=payload)
  return response.json()['id']

access_token = get_access_token(username, password)
autodiscoveryId = create_api(org_id, env_id, version, art_id, access_token)
print(autodiscoveryId)
