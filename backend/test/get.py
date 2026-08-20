import requests

response = requests.get('http://localhost:5000/api/actions/1/stats')
print(response.json())