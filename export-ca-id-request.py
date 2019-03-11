#-----------------------------------------
# export-ca-id-request.py
# 
# 
#-----------------------------------------

import os
import requests
from requests.auth import HTTPBasicAuth
import base64
import time

#-----------------------------------------

#Exe directory
exe_dir = os.path.dirname(os.path.abspath(__file__))

#-----------------------------------------

def generate_new_token(refresh_token, app_id, shared_secret):

    a = app_id + ':' + shared_secret
    encoded_auth = base64.b64encode(bytes(a, 'utf-8')).decode("ascii")
    url = 'https://api.channeladvisor.com/oauth2/token'
    
    h = {
    'Authorization':'Basic ' + encoded_auth ,
    'Cache-Control':'no-cache',
    'Content-Type':'application/x-www-form-urlencoded'
    }
    data = {
    'grant_type':'refresh_token',
    'refresh_token':refresh_token
    }

    r = requests.post(url, headers=h, data=data)
    return r

def request_id_export(auth_token):

   #url = 'https://api.channeladvisor.com/v1/ProductExport?&profileid=12002770&$filter=substringof%28SKU%2C%27MGZ-0004-OV%27%29'
    url = 'https://api.channeladvisor.com/v1/ProductExport?&profileid=12002770'
    
    h = {
    'Authorization':'Bearer ' + auth_token,
    'Cache-Control':'no-cache',
    'Content-Type':'text/plain'
    }
    data = "ID,Sku"

    r = requests.post(url, headers=h, data=data)
    return r

#-----------------------------------------

#ID & Token
app_id = 'ibz0g7c5ddjs9bqrgpzhk02qf2mcrq8v'
secret_key = 'xvMvRYfG40qPjyTlh67-dg'
refresh_token = 'ciiTQEhOOuHTTVpsAlt2sf2vKvVb4jNMMuZr5iOXXTc'

#-----------------------------------------

#Get refresh token
token = generate_new_token(refresh_token, app_id, secret_key)
auth_token = token.json().get('access_token')
r = request_id_export(auth_token)
res_token = r.json().get('Token')
res_file_url = r.json().get('ResponseFileUrl')
print(r.text)
print(res_token)
print(res_file_url)

#Check the status of export file
while res_file_url == None:
    
    time.sleep(60)

    url = 'https://api.channeladvisor.com/v1/ProductExport?token=' + res_token
    h = {
    'Authorization':'Bearer ' + auth_token,
    'Cache-Control':'no-cache'
    }

    r2 = requests.get(url, headers=h)
    res_file_url = r2.json().get('ResponseFileUrl')
    print(res_file_url)

#Zipファイルダウンロード
r = requests.get(res_file_url)
download_file = exe_dir + '/id.zip'
with open(download_file, 'wb') as f:  
    f.write(r.content)

print("Complete")

#-----------------------------------------