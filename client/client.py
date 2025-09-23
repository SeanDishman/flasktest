import requests

url = 'https://flasktest-0b6f.onrender.com/validate'

payload = {
    "hwid": "123456"
}

response = requests.post(url, json=payload)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")
