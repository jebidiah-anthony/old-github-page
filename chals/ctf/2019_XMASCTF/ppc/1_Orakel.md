---
layout: menu
title: "Orakel [ppc 152]"
Description: "X-MAS CTF 2019 [Professional Programming & Coding] Orakel (152 pts)"
header-img: "chals/ctf/2019_XMASCTF/xmas_ctf_2019.png"
tags: [xmas, x-mas, xmas ctf, x-mas ctf, 2019, ctf, challenge, writeup, write-up, solution, programming, coding, professional programming and coding, ppc, word search]
---

# <span style="color:red">Orakel (152 pts)</span>

---

## PART 1 : CHALLENGE DESCRIPTION

```
We have finally linked up with the famous Lapland Oracle, that knows and sees all!
Can you guess his secret word?

Remote server: challs.xmas.htsp.ro 13000
Authors: Milkdrop, Gabies
```

---

## PART 2 : GETTING THE FLAG

Connecting to the given server using __`netcat`__ gives:

```

                                     ,,,,
                                  ,########,
                                 ############
                                |############|
                                 ############
                                  "########"
                                     """"

                     |\___/|
                     | " " |                    ~ ORAKEL ~
              ,===__/( \ / )\__===,        THE LAPLAND  ORACLE
             /     """ (") """     \
            /           "           \
            |   \_____=   =_____/   |
      ,==._/    /\     /^\     /\    \_.==,
     |   _  __/"  \   |] [|   /  "\__  _   |
      555 """      |  |] [|  |      """ 555
"""""""""""""""""""###########""""""""""""""""""""""""""""""""""""""""""""
--- ,#######   ,#############, ,########  ___     _________
 -- #####################################"       _____     _________
    "###" #######################" ____     ___   _____           __
  ---_____  "#############   _           _________     ____
  ______     ##########        ______                _______
         ____"##  "##   _________            ___        ________  _____
    ___       ____    __     _________            _______



Hello child.

> I will give you the True Flag you seek, but for that you must pass my test:
I will think of a word of great length, known only by the gods that roam Lapland.
You must guess which word I am thinking of, but only under a limited number of [1000] tries.
In order to make this possible for you, I will tell you how close you are to my word through a number.
The higher the number, the further you are from my word.
If the number is 0, then you have found it.

Good Luck.
```

The challenge is to find the word the Lapland Oracle thinks of in <strong style="color:orange">a thousand tries or less</strong>. The <strong style="color:orange">guesses given are scored</strong> which tells you how close you really are to the actual word.

I created a simple script to find the "word" is as follows:

```py
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
```

From my observations, the length of the word and the actual "word" changes every new connection to the remote server. The length ranges consistently from <strong style="color:orange">91-101 characters</strong> and finding out how long the word is reduces the score from around 25000-30000 to 6000-8000 so that is what I did first:

```py
def findWordLength():

    string = "a" * 91
    prev_score = 1000000
    for i in range(0, 15):
    
        score = sendString(string + ("a" * i))

        if prev_score < score: 
            string += ("a" * (i - 1))
            return string, prev_score

        else: prev_score = score

```

The string is initialized as a string of "<strong>`a`</strong>"s and returned along with its score.

After figuring out the word length, I began somehow bruteforcing what each character of the word could be. 

```py
    # ...omitted...

    log.info("FINDING THE WORD")

    string = list(string)

    chars_lower = "abcdefghijklmnopqrstuvwxyz"
    string, score = findChars(string, chars_lower, score)

    chars_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[::-1]
    string, score = findChars(string, chars_upper, score)

    # ...omitted...
```

The search begins with lowercase letters begins from lowercase letters starting from <strong style="color:orange">a-z</strong> then uppercase letters from <strong style="color:orange">Z-A</strong>

```py
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

```

I tried my best to cut down the attempts to search for the right character without implementing a binary search algorithm. Using every single character each attempt would amount, at the worst case, to <strong style="color:red">52^length</strong> which exceeds a thousand by so much which is why <strong style="color:orange">I cut the character set in half (lowercase and uppercase)</strong> and <strong style="color:orange">traversed each character sets by increments of 2</strong>. 

> If, for example, the desired character is "s", the function would traverse throught the character set like this `b -> d -> f -> h -> j -> l -> n -> p -> r -> t` and since the traversal stopped at `t`, then the only possible characters are `r` and `s`. This is further narrowed down that if `r` and `t` have equal scores during checking, then the scoring must be `r` > `s` < `t` leaving `s` as the only option.

> Since the function will no longer iterate after `a` if the character is an uppercase letter, the worst case for both function calls becomes __`13`__ attempts for lowercase characters and __`14`__ attempts for uppercase letters. The code I wrote hinges on the possibility that all "words" generated have high entropy.

If after iterating through the lowercase letters, the character is still an <strong>"a"</strong>, there is a possibility that that character might be an uppercase letter and the reason why uppercase letters are traversed differently is that <strong>"Z"</strong> seems to have a closer score to <strong>"a"</strong> as compared to <strong>"A"</strong>.

Lastly, a few corrections are made if the program mistakenly turns a __`Z`__ to __`Y`__ and an __`a`__ to __`Z`__:

```py
def fixWordChar(string, index, new_char, score):
    
    temp = string[index]
    string[index] = new_char

    char_score = sendString("".join(string))
    print(guess_ctr, "%04d" % (score), "%04d" % (char_score), "".join(string))

    if score < char_score: return temp, score
    else: return string[index], char_score

def main():

    # ...omitted...

    log.info("CORRECTING SOME CHARACTERS")

    for i in range(0, len(string)):

        if string[i] == "Y" and score != 0: 
            string[i], score = fixWordChar(string, i, "Z", score)

        if string[i] == "Z" and score != 0: 
            string[i], score = fixWordChar(string, i, "a", score)

    # ...omitted...
```

Now, running the program:

```shell
[+] Opening connection to challs.xmas.htsp.ro on port 13000: Done
=====================================================================
[*] The word is 101 characters long.
=====================================================================
[*] FINDING THE WORD
('013', '7273', 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('024', '7171', 'asaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('025', '7171', 'asaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('026', '7171', 'asaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('035', '7093', 'asaaoaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('046', '6977', 'asaaotaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('047', '6977', 'asaaotaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('048', '6977', 'asaaotaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('060', '6881', 'asaaotaavaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('061', '6881', 'asaaotaavaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('073', '6769', 'asaaotaavauaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('075', '6767', 'asaaotaavaubaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('076', '6767', 'asaaotaavaubaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('077', '6767', 'asaaotaavaubaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('078', '6767', 'asaaotaavaubaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('091', '6650', 'asaaotaavaubaaawaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('092', '6650', 'asaaotaavaubaaawaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('103', '6553', 'asaaotaavaubaaawataaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('113', '6467', 'asaaotaavaubaaawatqaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('125', '6357', 'asaaotaavaubaaawatqvaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('133', '6282', 'asaaotaavaubaaawatqvnaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('134', '6282', 'asaaotaavaubaaawatqvnaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('141', '6229', 'asaaotaavaubaaawatqvnalaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('142', '6229', 'asaaotaavaubaaawatqvnalaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('143', '6229', 'asaaotaavaubaaawatqvnalaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('148', '6197', 'asaaotaavaubaaawatqvnalaagaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('154', '6147', 'asaaotaavaubaaawatqvnalaagjaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('155', '6147', 'asaaotaavaubaaawatqvnalaagjaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('156', '6147', 'asaaotaavaubaaawatqvnalaagjaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('157', '6147', 'asaaotaavaubaaawatqvnalaagjaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('158', '6147', 'asaaotaavaubaaawatqvnalaagjaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('162', '6136', 'asaaotaavaubaaawatqvnalaagjaaaaeaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('163', '6136', 'asaaotaavaubaaawatqvnalaagjaaaaeaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('170', '6094', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('171', '6094', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('172', '6094', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('181', '6001', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('194', '5886', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('195', '5886', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('196', '5886', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('197', '5886', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('210', '5756', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('216', '5697', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('217', '5697', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('219', '5693', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('227', '5613', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('232', '5579', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('243', '5470', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('244', '5470', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('245', '5470', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('248', '5453', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('261', '5348', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('262', '5348', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('267', '5313', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('268', '5313', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('269', '5313', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('270', '5313', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('271', '5313', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('276', '5273', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('277', '5273', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('278', '5273', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('279', '5273', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('290', '5171', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('291', '5171', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('292', '5171', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('306', '5043', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('313', '4980', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataaykaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('321', '4914', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('334', '4787', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('337', '4770', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('338', '4770', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('339', '4770', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('343', '4744', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('344', '4744', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('345', '4744', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('346', '4744', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
('354', '4694', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamaaaaaaaaaaaaaaaaaaaaaaaa')
('367', '4585', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzaaaaaaaaaaaaaaaaaaaaaaa')
('374', '4520', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlaaaaaaaaaaaaaaaaaaaaaa')
('382', '4443', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmaaaaaaaaaaaaaaaaaaaaa')
('387', '4407', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaaaaaaaaaaaaaaaaaaa')
('388', '4407', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaaaaaaaaaaaaaaaaaaa')
('389', '4407', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaaaaaaaaaaaaaaaaaaa')
('390', '4407', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaaaaaaaaaaaaaaaaaaa')
('404', '4259', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayaaaaaaaaaaaaaaaa')
('408', '4230', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaaaaaaaaaaaaaa')
('409', '4230', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaaaaaaaaaaaaaa')
('410', '4230', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaaaaaaaaaaaaaa')
('413', '4202', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaadaaaaaaaaaaaa')
('416', '4187', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaaaaaaaaaaa')
('417', '4187', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaaaaaaaaaaa')
('418', '4187', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaaaaaaaaaaa')
('422', '4158', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaafaaaaaaaa')
('431', '4081', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaafpaaaaaaa')
('432', '4081', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaafpaaaaaaa')
('437', '4028', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaafpahaaaaa')
('438', '4028', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaafpahaaaaa')
('439', '4028', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaafpahaaaaa')
('450', '3927', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaafpahaasaa')
('463', '3794', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaafpahaaswa')
('470', '3725', 'asaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaafpahaaswl')
('479', '3638', 'Lsaaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaafpahaaswl')
('480', '3638', 'LsZaotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaafpahaaswl')
('489', '3574', 'LsZLotaavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaafpahaaswl')
('498', '3478', 'LsZLotKavaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaafpahaaswl')
('507', '3399', 'LsZLotKKvaubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaafpahaaswl')
('512', '3348', 'LsZLotKKvSubaaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaafpahaaswl')
('520', '3259', 'LsZLotKKvSubMaawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaafpahaaswl')
('521', '3259', 'LsZLotKKvSubMZawatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaafpahaaswl')
('529', '3185', 'LsZLotKKvSubMZMwatqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaafpahaaswl')
('536', '3125', 'LsZLotKKvSubMZMwPtqvnalaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaafpahaaswl')
('545', '3046', 'LsZLotKKvSubMZMwPtqvnKlaagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaafpahaaswl')
('555', '2944', 'LsZLotKKvSubMZMwPtqvnKlJagjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaafpahaaswl')
('558', '2932', 'LsZLotKKvSubMZMwPtqvnKlJWgjaaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaafpahaaswl')
('565', '2870', 'LsZLotKKvSubMZMwPtqvnKlJWgjOaaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaafpahaaswl')
('569', '2833', 'LsZLotKKvSubMZMwPtqvnKlJWgjOVaaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaafpahaaswl')
('579', '2754', 'LsZLotKKvSubMZMwPtqvnKlJWgjOVJaeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaafpahaaswl')
('583', '2731', 'LsZLotKKvSubMZMwPtqvnKlJWgjOVJVeakaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaafpahaaswl')
('594', '2607', 'LsZLotKKvSubMZMwPtqvnKlJWgjOVJVeGkaaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaafpahaaswl')
('599', '2555', 'LsZLotKKvSubMZMwPtqvnKlJWgjOVJVeGkSaoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaafpahaaswl')
('610', '2439', 'LsZLotKKvSubMZMwPtqvnKlJWgjOVJVeGkSHoxaaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaafpahaaswl')
('612', '2439', 'LsZLotKKvSubMZMwPtqvnKlJWgjOVJVeGkSHoxYaaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaafpahaaswl')
('617', '2399', 'LsZLotKKvSubMZMwPtqvnKlJWgjOVJVeGkSHoxYTaxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaafpahaaswl')
('627', '2323', 'LsZLotKKvSubMZMwPtqvnKlJWgjOVJVeGkSHoxYTIxiabnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaafpahaaswl')
('628', '2323', 'LsZLotKKvSubMZMwPtqvnKlJWgjOVJVeGkSHoxYTIxiZbnhsaacwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaafpahaaswl')
('638', '2228', 'LsZLotKKvSubMZMwPtqvnKlJWgjOVJVeGkSHoxYTIxiZbnhsJacwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaafpahaaswl')
('643', '2177', 'LsZLotKKvSubMZMwPtqvnKlJWgjOVJVeGkSHoxYTIxiZbnhsJScwagaaaagaaataayknwdaafaaamzlmgaaayfaaddaafpahaaswl')
('655', '2077', 'LsZLotKKvSubMZMwPtqvnKlJWgjOVJVeGkSHoxYTIxiZbnhsJScwFgaaaagaaataayknwdaafaaamzlmgaaayfaaddaafpahaaswl')
('666', '1975', 'LsZLotKKvSubMZMwPtqvnKlJWgjOVJVeGkSHoxYTIxiZbnhsJScwFgGaaagaaataayknwdaafaaamzlmgaaayfaaddaafpahaaswl')
('669', '1952', 'LsZLotKKvSubMZMwPtqvnKlJWgjOVJVeGkSHoxYTIxiZbnhsJScwFgGWaagaaataayknwdaafaaamzlmgaaayfaaddaafpahaaswl')
('677', '1876', 'LsZLotKKvSubMZMwPtqvnKlJWgjOVJVeGkSHoxYTIxiZbnhsJScwFgGWMagaaataayknwdaafaaamzlmgaaayfaaddaafpahaaswl')
('682', '1822', 'LsZLotKKvSubMZMwPtqvnKlJWgjOVJVeGkSHoxYTIxiZbnhsJScwFgGWMSgaaataayknwdaafaaamzlmgaaayfaaddaafpahaaswl')
('684', '1804', 'LsZLotKKvSubMZMwPtqvnKlJWgjOVJVeGkSHoxYTIxiZbnhsJScwFgGWMSgYaataayknwdaafaaamzlmgaaayfaaddaafpahaaswl')
('697', '1694', 'LsZLotKKvSubMZMwPtqvnKlJWgjOVJVeGkSHoxYTIxiZbnhsJScwFgGWMSgYDataayknwdaafaaamzlmgaaayfaaddaafpahaaswl')
('710', '1561', 'LsZLotKKvSubMZMwPtqvnKlJWgjOVJVeGkSHoxYTIxiZbnhsJScwFgGWMSgYDDtaayknwdaafaaamzlmgaaayfaaddaafpahaaswl')
('723', '1431', 'LsZLotKKvSubMZMwPtqvnKlJWgjOVJVeGkSHoxYTIxiZbnhsJScwFgGWMSgYDDtCayknwdaafaaamzlmgaaayfaaddaafpahaaswl')
('729', '1381', 'LsZLotKKvSubMZMwPtqvnKlJWgjOVJVeGkSHoxYTIxiZbnhsJScwFgGWMSgYDDtCQyknwdaafaaamzlmgaaayfaaddaafpahaaswl')
('740', '1265', 'LsZLotKKvSubMZMwPtqvnKlJWgjOVJVeGkSHoxYTIxiZbnhsJScwFgGWMSgYDDtCQyknwdHafaaamzlmgaaayfaaddaafpahaaswl')
('744', '1226', 'LsZLotKKvSubMZMwPtqvnKlJWgjOVJVeGkSHoxYTIxiZbnhsJScwFgGWMSgYDDtCQyknwdHVfaaamzlmgaaayfaaddaafpahaaswl')
('749', '1176', 'LsZLotKKvSubMZMwPtqvnKlJWgjOVJVeGkSHoxYTIxiZbnhsJScwFgGWMSgYDDtCQyknwdHVfSaamzlmgaaayfaaddaafpahaaswl')
('757', '1119', 'LsZLotKKvSubMZMwPtqvnKlJWgjOVJVeGkSHoxYTIxiZbnhsJScwFgGWMSgYDDtCQyknwdHVfSMamzlmgaaayfaaddaafpahaaswl')
('758', '1119', 'LsZLotKKvSubMZMwPtqvnKlJWgjOVJVeGkSHoxYTIxiZbnhsJScwFgGWMSgYDDtCQyknwdHVfSMZmzlmgaaayfaaddaafpahaaswl')
('771', '0982', 'LsZLotKKvSubMZMwPtqvnKlJWgjOVJVeGkSHoxYTIxiZbnhsJScwFgGWMSgYDDtCQyknwdHVfSMZmzlmgCaayfaaddaafpahaaswl')
('778', '0929', 'LsZLotKKvSubMZMwPtqvnKlJWgjOVJVeGkSHoxYTIxiZbnhsJScwFgGWMSgYDDtCQyknwdHVfSMZmzlmgCPayfaaddaafpahaaswl')
('789', '0827', 'LsZLotKKvSubMZMwPtqvnKlJWgjOVJVeGkSHoxYTIxiZbnhsJScwFgGWMSgYDDtCQyknwdHVfSMZmzlmgCPGyfaaddaafpahaaswl')
('802', '0674', 'LsZLotKKvSubMZMwPtqvnKlJWgjOVJVeGkSHoxYTIxiZbnhsJScwFgGWMSgYDDtCQyknwdHVfSMZmzlmgCPGyfAaddaafpahaaswl')
('807', '0626', 'LsZLotKKvSubMZMwPtqvnKlJWgjOVJVeGkSHoxYTIxiZbnhsJScwFgGWMSgYDDtCQyknwdHVfSMZmzlmgCPGyfASddaafpahaaswl')
('820', '0482', 'LsZLotKKvSubMZMwPtqvnKlJWgjOVJVeGkSHoxYTIxiZbnhsJScwFgGWMSgYDDtCQyknwdHVfSMZmzlmgCPGyfASddAafpahaaswl')
('833', '0351', 'LsZLotKKvSubMZMwPtqvnKlJWgjOVJVeGkSHoxYTIxiZbnhsJScwFgGWMSgYDDtCQyknwdHVfSMZmzlmgCPGyfASddACfpahaaswl')
('843', '0252', 'LsZLotKKvSubMZMwPtqvnKlJWgjOVJVeGkSHoxYTIxiZbnhsJScwFgGWMSgYDDtCQyknwdHVfSMZmzlmgCPGyfASddACfpIhaaswl')
('853', '0149', 'LsZLotKKvSubMZMwPtqvnKlJWgjOVJVeGkSHoxYTIxiZbnhsJScwFgGWMSgYDDtCQyknwdHVfSMZmzlmgCPGyfASddACfpIhIaswl')
('864', '0030', 'LsZLotKKvSubMZMwPtqvnKlJWgjOVJVeGkSHoxYTIxiZbnhsJScwFgGWMSgYDDtCQyknwdHVfSMZmzlmgCPGyfASddACfpIhIGswl')
=====================================================================
[*] CORRECTING SOME CHARACTERS
(865, '0030', '0026', 'LsaLotKKvSubMZMwPtqvnKlJWgjOVJVeGkSHoxYTIxiZbnhsJScwFgGWMSgYDDtCQyknwdHVfSMZmzlmgCPGyfASddACfpIhIGswl')
(866, '0026', '0030', 'LsbLotKKvSubMZMwPtqvnKlJWgjOVJVeGkSHoxYTIxiZbnhsJScwFgGWMSgYDDtCQyknwdHVfSMZmzlmgCPGyfASddACfpIhIGswl')
(867, '0026', '0020', 'LsaLotKKvSubMaMwPtqvnKlJWgjOVJVeGkSHoxYTIxiZbnhsJScwFgGWMSgYDDtCQyknwdHVfSMZmzlmgCPGyfASddACfpIhIGswl')
(868, '0020', '0026', 'LsaLotKKvSubMbMwPtqvnKlJWgjOVJVeGkSHoxYTIxiZbnhsJScwFgGWMSgYDDtCQyknwdHVfSMZmzlmgCPGyfASddACfpIhIGswl')
(869, '0020', '0012', 'LsaLotKKvSubMaMwPtqvnKlJWgjOVJVeGkSHoxZTIxiZbnhsJScwFgGWMSgYDDtCQyknwdHVfSMZmzlmgCPGyfASddACfpIhIGswl')
(870, '0012', '0020', 'LsaLotKKvSubMaMwPtqvnKlJWgjOVJVeGkSHoxaTIxiZbnhsJScwFgGWMSgYDDtCQyknwdHVfSMZmzlmgCPGyfASddACfpIhIGswl')
(871, '0012', '0002', 'LsaLotKKvSubMaMwPtqvnKlJWgjOVJVeGkSHoxZTIxiabnhsJScwFgGWMSgYDDtCQyknwdHVfSMZmzlmgCPGyfASddACfpIhIGswl')
(872, '0002', '0012', 'LsaLotKKvSubMaMwPtqvnKlJWgjOVJVeGkSHoxZTIxibbnhsJScwFgGWMSgYDDtCQyknwdHVfSMZmzlmgCPGyfASddACfpIhIGswl')
(873, '0002', '0010', 'LsaLotKKvSubMaMwPtqvnKlJWgjOVJVeGkSHoxZTIxiabnhsJScwFgGWMSgZDDtCQyknwdHVfSMZmzlmgCPGyfASddACfpIhIGswl')
(874, '0002', '0000', 'LsaLotKKvSubMaMwPtqvnKlJWgjOVJVeGkSHoxZTIxiabnhsJScwFgGWMSgYDDtCQyknwdHVfSMamzlmgCPGyfASddACfpIhIGswl')
=====================================================================
[+] WORD FOUND: LsaLotKKvSubMaMwPtqvnKlJWgjOVJVeGkSHoxZTIxiabnhsJScwFgGWMSgYDDtCQyknwdHVfSMamzlmgCPGyfASddACfpIhIGswl
=====================================================================
[+] Masterfully done. Here is the True Flag: X-MAS{7hey_h4t3d_h1m_b3c4use_h3_sp0k3_th3_truth} 
=====================================================================
[*] Closed connection to challs.xmas.htsp.ro port 13000
```

---

## FLAG : __X-MAS{7hey_h4t3d_h1m_b3c4use_h3_sp0k3_th3_truth}__

