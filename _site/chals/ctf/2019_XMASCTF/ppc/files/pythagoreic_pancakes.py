from pwn import *
import hashlib

pwnable = remote("challs.xmas.htsp.ro", 14004)
print("====================================================================")
log.info("GENERATING PRIMITIVE PYTHAGOREAN TRIPLES")

def getGCD(sml_num, lrg_num): # Euclidian Algorithm

    while sml_num > 0:
        
        r = lrg_num % sml_num
        lrg_num = sml_num
        sml_num = r

    return lrg_num

triples = list()
for x in range(2, 5001):

    for y in range(1, x):

        if x % 2 == 1 and y % 2 == 1:
            if getGCD(y, x) == 1:
                # Euclid's formula for determining Pythagorean Triples
                a = x*y
                b = (x**2 - y**2)/2
                c = (x**2 + y**2)/2

                #distance_from_origin = a**2 + b**2 + c**2
                triple = sorted([a, b ,c])

#                triples.append([x, y, triple, distance_from_origin])
                triples.append([x, y, triple])

#triples = sorted(triples, key=lambda x: (x[3], x[2][2], x[2][1]))
triples = sorted(triples, key=lambda x: (x[2][2], x[2][1]))
#triples = sorted(triples, key=lambda x: x[3])

log.success("%d PRIMITIVE PYTHAGOREAN TRIPLES GENERATED" % (len(triples)))
print("====================================================================")

request = pwnable.recvline()
log.info(request)
criterion = request[-7:-1]
log.info("FINDING PARTIAL HASH COLLISION WITH \"%s\"" % (criterion))

characters = '0123456789abcdef'
length = 16

string = characters[0] * length
char_indices =  [0 for x in string]

while char_indices.count(len(characters)-1) != len(char_indices):

    hexString = "".join([characters[x] for x in char_indices])

    sha256 = hashlib.sha256()
    sha256.update(bytes(hexString.decode("hex")))
    sha256_hex = str(sha256.hexdigest())

    if sha256_hex[-6:] == criterion:
        log.success("PARTIAL MATCH FOUND: %s" % (hexString.decode("hex")))
        log.success("SHA256 HASH: %s" % (sha256_hex))
        log.info("SENDING HEX STRING: %s" % (hexString))
        pwnable.sendline(hexString)
        break

    char_indices[-1] += 1
    for x in range(len(string)-1, 0, -1):

        if char_indices[x] == len(characters): 
            char_indices[x] = 0
            char_indices[x-1] += 1 

pwnable.recvline()
log.success(pwnable.recvline())
for i in range(0, 5): pwnable.recvline()
print("===================================================================")

for i in range(0, 10):
    log.info(pwnable.recvline())
    challenge = pwnable.recvline()
    log.info(challenge)

    nth_prim_triple = int(challenge.split(" ")[3].split("-")[0])
    triple = triples[nth_prim_triple - 1][2]

    log.info("%d-TH PRIMITIVE PYTHAGOREAN TRIPLE: %d, %d, %d" % (nth_prim_triple, triple[0], triple[1], triple[2]))

    pwnable.sendline("%d,%d,%d" % (triple[0], triple[1], triple[2]))
    log.success(pwnable.recvline())
    print("===================================================================")

log.info(pwnable.recvline())
log.success(pwnable.recvline())
print("===================================================================")
