---
layout: menu
---

## <span style="color:red">Super Duper AES</span>

---

### PART 1 : CHALLENGE DESCRIPTION

```
The Advanced Encryption Standard (AES) has got to go. Spencer just 
invented the Super Duper Advanced Encryption Standard (SDAES), and 
it's 100% unbreakable. AES only performs up to 14 rounds of 
substitution and permutation, while SDAES performs 10,000. That's so 
secure, SDAES doesn't even use a key!
```

---

### PART 2 : GIVEN FILES

#### __[>]__ [sdaes.py](./files/SuperDuperAES/sdaes.py)
#### __[>]__ [cipher.txt](./files/SuperDuperAES/cipher.txt)
```
d59fd3f37182486a44231de4713131d20324fbfe80e91ae48658ba707cb84841972305fc3e0111c753733cf2
```

---

### PART 3 : PROGRAM FLOW

1. A plaintext is passed as an argument when running `sdaes.py`:
   ```console
   $ python3 sdaes.py "<plaintext>"
   ```

2. The plaintext is padded if necessary to have a lenght with a multiple of 4:
   ```py
   def pad(message):
       numBytes = 4-(len(message)%4)
       return message + numBytes * chr(numBytes)
   ```

3. The plaintext is converted to hex then separated into blocks with a length of 8 nibbles (4 bytes).

4. Each block goes through a substitution function
   ```py
   def substitute(hexBlock):
       substitutedHexBlock = ""
       substitution =  [8, 4, 15, 9, 3, 14, 6, 2, 
                       13, 1, 7, 5, 12, 10, 11, 0]
       for hexDigit in hexBlock:
           newDigit = substitution[int(hexDigit, 16)]
           substitutedHexBlock += hex(newDigit)[2:]
       return substitutedHexBlock
   ```
   __NOTE(S)__:
   1. Each nibble is substituted depending on its corresponding value in the `substitution` array.

5. After the substitution, the block undergoes permutation:
   ```py
   def permute(hexBlock):
       permutation =   [6, 22, 30, 18, 29, 4, 23, 19, 
                       15, 1, 31, 11, 28, 14, 25, 2, 
                       27, 12, 21, 26, 10, 16, 0, 24,
                        7, 5, 3, 20, 13, 9, 17, 8]
       block = int(hexBlock, 16)
       permutedBlock = 0
       for i in range(32):
           bit = (block & (1 << i)) >> i
           permutedBlock |= bit << permutation[i]
       return hexpad(hex(permutedBlock)[2:])
   ```
   __NOTE(S)__:
   1. It checks if a __`bit`__ is turned on or equal to `1`.
   2. The bit corresponding to the value in the `permutation` array is turned on if the value of `bit` is 1.

6. Steps __#3__ to __#5__ are repeated 10,000 times to produce the ciphertext.

---

### PART 4 : GETTING THE FLAG

1. Reverse the __`permute()`__ function:
   1. Consider __`permutationBlock`__ as a string of 32 0s:
      ```
      00000000000000000000000000000000
      ```
   2. __`bit`__ only returns `1` or `0`:
      - __HYPOTHETICALLY:__ if the __`32nd`, `28th`, `16th`,__ and __`8th`__ bit (from the right) from the current block are turned on:
        ```py
        >>> permutation = [...omitted..]
        >>> permutedBlock = 0
        >>> format(permutedBlock, "032b")
        '00000000000000000000000000000000'
        >>>
        >>> bit = 1  # bit is set to 1 since the test bits below are assumed to be turned on.
        >>>
        >>> permutedBlock |= bit << permutation[32 - 1]  # permutation[32 - 1] => 8
        >>> format(permutedBlock, "032b")
        '00000000000000000000000100000000'
        >>>
        >>> permutedBlock |= bit << permutation[28 - 1]  # permutation[28 - 1] => 20
        >>> format(permutedBlock, "032b")
        '00000000000100000000000100000000'
        >>>
        >>> permutedBlock |= bit << permutation[16 - 1]  # permutation[16 - 1] => 2
        >>> format(permutedBlock, "032b")
        '00000000000100000000000100000100'
        >>>
        >>> permutedBlock |= bit << permutation[8 - 1]   # permutation[8 - 1]  => 19
        >>> format(permutedBlock, "032b")
        '00000000000110000000000100000100'
        ```
      - __`10001000000000001000000010000000`__ was just remapped to __`00000000000110000000000100000100`__
      - The permutation function basically checks if a bit is turned on in the ciphertext blockthen remaps them to a different position based on the __`permutation`__ array.
      - There will be no conflict in checking if a bit was originally turned on since each of the original set of bits could only be mapped to a corresponding unique position after the permutation.

   3. A function definition for undoing the permutation:
      ```python
      def permute(hexBlock):
          permutation =   [6, 22, 30, 18, 29, 4, 23, 19, 15, 1, 31, 11, 28, 14, 25, 2, 27, 12, 21, 26, 10, 16, 0, 24, 7, 5, 3, 20, 13, 9, 17, 8]
          sub_block = ["0" for i in range(32)]
          for i in range(31, -1, -1):
              enc_block = format(int(hexBlock, 16), "032b")

              if enc_block[i] == "1": 
                  bit = permutation.index(31 - i)
                  sub_block[bit] = "1"
        
          sub_block = "".join(sub_block[::-1])

          return hexpad(hex(int(sub_block, 2))[2:])
      ```

2. Reverse the __`substitute()`__ function:
   1. The nibbles on the plaintext block are substituted based on the __`substitution`__ array:
      
      0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | A | B | C | D | E | F 
      --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---
      8 | 4 | F | 9 | 3 | E | 6 | 2 | D | 1 | 7 | 5 | C | A | B | 0

   2. Just remap the nibbles back to their original positions:

      0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | A | B | C | D | E | F 
      --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---
      F | 9 | 7 | 4 | 1 | B | 6 | A | 0 | 3 | D | E | C | 8 | 5 | 2

3. Put everything together:
   ```py
   from binascii import hexlify,unhexlify

   def hexpad(hexBlock):
       numZeros = 8 - len(hexBlock)
       return numZeros*"0" + hexBlock
   
   def substitute(hexBlock):
       substitutedHexBlock = ""
       substitution = [15, 9, 7, 4, 1, 11, 6, 10, 0, 3, 13, 14, 12, 8, 5, 2]
       for hexDigit in hexBlock:
           newDigit = substitution[int(hexDigit, 16)]
           substitutedHexBlock += hex(newDigit)[2:]
   
       return substitutedHexBlock
   
   
   def permute(hexBlock):
       permutation =   [6, 22, 30, 18, 29, 4, 23, 19, 15, 1, 31, 11, 28, 14, 25, 2, 27, 12, 21, 26, 10, 16, 0, 24, 7, 5, 3, 20, 13, 9, 17, 8]
       sub_block = ["0" for i in range(32)]
       for i in range(31, -1, -1):
           enc_block = format(int(hexBlock, 16), "032b")
   
           if enc_block[i] == "1": 
               bit = permutation.index(31 - i)
               sub_block[bit] = "1"
           
       sub_block = "".join(sub_block[::-1])
   
       return hexpad(hex(int(sub_block, 2))[2:])
   
   
   def round(hexMessage):
       numBlocks = len(hexMessage)//8
       permutedHexMessage = ""
       for i in range(numBlocks):
           permutedHexMessage += permute(hexMessage[8*i:8*i+8])
       substitutedHexMessage = ""
       for i in range(numBlocks):
           substitutedHexMessage += substitute(permutedHexMessage[8*i:8*i+8])
       return substitutedHexMessage
   
   
   if __name__ == "__main__":
   
       with open("cipher.txt", "r") as ciphertext:
           hexMessage = ciphertext.read()
           for i in range(10000):
               hexMessage = round(hexMessage)
        print(unhexlify(hexMessage).decode("utf-8"))
   ```
   __NOTE(S)__:
   1. Since the original process per round was substitute then permutate, the decryption should be permutation before substitution.

4. Run the decryption script:
   ```console
   $ python3 decrypt.py
     nactf{5ub5t1tut10n_p3rmutat10n_n33d5_a_k3y}
   ```
   __NOTE(S)__:
   1. The permutation and substitution functions will always be reversible for block ciphers especially if they are known.
   2. The vulnerability lies with the lack of key passed during encryption.
      - The number of rounds used during encryption would be irrelevant since the ciphertext produced without a key wouldn't really be "random" enough.

---

## FLAG : __nactf{5ub5t1tut10n_p3rmutat10n_n33d5_a_k3y}__
