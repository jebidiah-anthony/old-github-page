from pwn import *

pwnable = remote("challs.xmas.htsp.ro", 13000)
guess_ctr = 0

def sendString(string):
    
    pwnable.recvuntil("Tell me your guess: ")
    pwnable.sendline(string)
   
    global guess_ctr
    guess_ctr += 1
    
    out = pwnable.recvline()
    score = int(out.split(": ")[1])

    return score

def findWordLength():

    string = "a" * 91
    prev_score = 1000000
    for i in range(0, 15):
    
        score = sendString(string + ("a" * i))

        if prev_score < score: 
            string += ("a" * (i - 1))
            return string, prev_score

        else: prev_score = score

def findChars(string, charset, score):

    for i in range(0, len(string)):

        if string[i] == "a":
            best_char = charset[0]
            string[i] = charset[0]

            for x in range(1, (len(charset)/2)+1):

                string[i] = charset[x*2 - 1]
                char_score = sendString("".join(string))

                if score > char_score:
                    best_char = charset[x*2 - 1]
                    score = char_score

                elif score == char_score:
                    best_char = charset[charset.index(best_char) + 1]
                    string[i] = best_char        
                    score = sendString("".join(string))
                    break

                else: break

            string[i] = best_char
            print("%03d" % (guess_ctr), "%04d" % (score), "".join(string))             
    return string, score

def fixWordChar(string, index, new_char, score):
    
    temp = string[index]
    string[index] = new_char

    char_score = sendString("".join(string))
    print(guess_ctr, "%04d" % (score), "%04d" % (char_score), "".join(string))

    if score < char_score: return temp, score
    else: return string[index], char_score

def main():

    print "====================================================================="

    string, score = findWordLength()
    log.info("The word is %d characters long." % (len(string)))

    print "====================================================================="

    log.info("FINDING THE WORD")

    string = list(string)

    chars_lower = "abcdefghijklmnopqrstuvwxyz"
    string, score = findChars(string, chars_lower, score)

    chars_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[::-1]
    string, score = findChars(string, chars_upper, score)

    print "====================================================================="

    log.info("CORRECTING SOME CHARACTERS")

    for i in range(0, len(string)):

        if string[i] == "Y" and score != 0: 
            string[i], score = fixWordChar(string, i, "Z", score)

        if string[i] == "Z" and score != 0: 
            string[i], score = fixWordChar(string, i, "a", score)

#        if string[i] == "a" and score != 0: 
#            string[i], score = fixWordChar(string, i, "b", score)    

#        if string[i] == "B" and score != 0:
#            string[i], score = fixWordChar(string, i, "A", score)

        if score == 0: 
            print "====================================================================="
            log.success("WORD FOUND: %s" % ("".join(string)))
            print "====================================================================="
            pwnable.recvline()
            log.success(pwnable.recvline())

            print "====================================================================="
            break

    if score != 0 and guess_ctr < 1000: pwnable.interactive()

if __name__ == '__main__': main()

# X-MAS{7hey_h4t3d_h1m_b3c4use_h3_sp0k3_th3_truth}
