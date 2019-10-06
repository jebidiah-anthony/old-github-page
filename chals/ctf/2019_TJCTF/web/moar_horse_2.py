import requests as r

def check_link(target, curr, links):

    print(curr)

    req = r.get(target+curr)

    if "{" in req.text: 
        print(req.text)
        exit()

    if(req.text[319:361]) not in links:
        links.append(req.text[319:361])
        check_link(target, req.text[319:361], links) #BACKWARD

    if(req.text[473:515]) not in links:
        links.append(req.text[473:515])
        check_link(target, req.text[473:515], links) #FORWARD


target = "https://moar_horse_2.tjctf.org"
curr = "/4b043a01-a4b7-4141-8a99-fc94fe7e3778.html" #link of the 
links = ["/4b043a01-a4b7-4141-8a99-fc94fe7e3778.html"]

check_link(target, curr, links)

# FLAG:
# https://moar_horse_2.tjctf.org/3cf94f73-568f-4dbc-b185-d545aff438d6.html

# /4b043a01-a4b7-4141-8a99-fc94fe7e3778.html (START)
# /9443d5de-115c-40c6-a822-d1ce94ccd8e0.html
# /d954642d-abd9-4d3e-adcc-a69b7d853e5a.html
# /d383feb8-e6f9-4415-873e-8fbc80d1b862.html
# /9d63c5b1-477a-4fbc-8eba-ac080d33c814.html
# /d9609442-ae9e-4c37-9967-27508c16fb9b.html
# /25f5df29-8d24-40bb-a652-d65a13db249e.html
# /d565f6ef-c9cf-4030-b501-b6bf2aa2b6c5.html
# /ee4d8fe9-3170-4e75-bc38-46852a5cfd79.html
# /f007ecf9-e83c-4d16-b122-76eef4815c7a.html
# /ceba1b35-2788-462f-830b-76d8ac56f96d.html
# /42bc2fcc-d3f6-4de3-9b67-15a865d62cb8.html
# /77504246-70cd-4501-bea2-7ca7426f55e9.html
# /a07cb0d7-df0a-4b5e-9ba3-12fc002fb71a.html
# /9d3b0782-9323-49f8-a5f3-57abd07b82bc.html (BACKWARD)
# /4b043a01-a4b7-4141-8a99-fc94fe7e3778.html (START) <- beginning
# /e634644e-b802-496a-8bb5-0e0aac40779f.html (FORWARD)
# /f50f7e37-8ba7-43c6-9836-a6148831564e.html
# /ac2ecaa1-0dc9-47ae-b8f1-133d50e4af99.html
# /d6ca6b5d-c8be-4474-b612-407df5b4bb04.html
# /9552275b-c392-4f5c-ac0b-f6dd843bf94b.html
# /a0da2909-c757-4231-8075-f75ff2a2ce00.html
# /c9f7162a-2ce1-40d4-81a5-6a6f92d08c54.html
# /715a3c29-6834-4a01-a757-729aab193a62.html
# /c037b1ac-9d23-4a98-aab8-4667281509a1.html
# /e7795183-e817-48ce-bfa6-f69dc9b6d67f.html
# /b846555a-a1a5-49c2-8896-950145057e73.html
# /ce1b06c9-553b-4448-a6b7-887b6fb79615.html
# /f5bc4454-74bb-4594-8666-a58242cb53fb.html
# /d4fc331c-542a-46ed-8b37-a0c3c74c7b61.html
# /4b043a01-a4b7-4141-8a99-fc94fe7e3778.html (START)
