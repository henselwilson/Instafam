import requests

endpoint="http://127.0.0.1:8000/account/register"
data={
    'username':'henselwilson',
    'email':'henselwilson',
    'password':'Newuser123',
    'AccountType': 'pub'
}
result=requests.post(endpoint,json=data)
print(result.json())