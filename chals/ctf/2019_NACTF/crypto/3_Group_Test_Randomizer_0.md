---
layout: menu
---

## <span style="color:red">Dr. J's Group Test Randomizer #0</span>

---

### PART 1 : CHALLENGE DESCRIPTION

```
Dr. J created a fast pseudorandom number generator (prng) to 
randomly assign pairs for the upcoming group test. Leaf really wants 
to know the pairs ahead of time... can you help him and predict the 
next output of Dr. J's prng? Leaf is pretty sure that Dr. J is using 
the middle-square method.

nc shell.2019.nactf.com 31425

The server is running the code in class-randomizer-0.c. Look at the 
function nextRand() to see how numbers are being generated!
```

---

### PART 2 : GIVEN FILES

#### __[>]__ [class-randomizer-0.c](./files/class-randomizer-0.c)

---

### PART 3 : PROGRAM FLOW

1. A seed is initialized:
   ```c
   uint64_t seed = 0;

   void init_seed() {
     uint64_t r1 = (uint64_t) randombytes_random();
     uint64_t r2 = (uint64_t) randombytes_random();
     seed = (r1 << 32) + r2;
   }
   ```
   __NOTE(S)__:
   1. The generated seed has a maximum value of __`0xffffffff`__.

2. An actions menu is presented to the user:
   ```c
   printf("\nWelcome to Dr. J's Random Number Generator v1! \n"
   "[r] Print a new random number \n"
   "[g] Guess the next two random numbers and receive the flag! \n"
   "[q] Quit \n\n");
   ```
   1. __`[r]`__ generates a new random number:
      ```c
      uint64_t nextRand() {
        // Keep the 8 middle digits from 5 to 12 (inclusive) and square.
        seed = getDigits(seed, 5, 12);
        seed *= seed;
        return seed;
      }
      ```
      __NOTE(S)__:
      1. The __5th__ to the __8th__ digits from the right of the seed is squared.
      2. The squared number is now the new seed.

   2. __`[g]`__ lets the user guess the next two "random" numbers to get the flag.

   3. __`[q]`__ lets the user exit the program.

---

### PART 4 : GETTING THE FLAG

1. Run the program:
   ```console
   $ nc shell.2019.nactf.com 31425

     Welcome to Dr. J's Random Number Generator v1! 
     [r] Print a new random number 
     [g] Guess the next two random numbers and receive the flag! 
     [q] Quit 

   $ > r
     5339808891408016
   $ > g

     Guess the next two random numbers for a flag! You have a 0.0000000000000000000000000000001% chance of guessing both correctly... Good luck!
     Enter your first guess:
   $ > 6543052969939600

     Wow, lucky guess... You won't be able to guess right a second time.
     Enter your second guess:
   $ > 28058134842049

     What? You must have psychic powers... Well here's your flag: nactf{1_l0v3_chunky_7urn1p5}
   ```
   __NOTE(S)__:
   1. The vulnerability lies with the fact that the current seed is output as the "random" number generated"
   2. That and the fact that the next seed is just the square of 8 middle digits from the current seed.
   3. Generating the next "random" numbers using the `python3` console:
      ```py
      >>> curr = 5339808891408016
      >>> curr = int(str(curr)[-12:-4])**2
      >>> curr
      6543052969939600
      >>> curr = int(str(curr)[-12:-4])**2
      >>> curr
      28058134842049
      ``` 

---

## FLAG : __nactf{1_l0v3_chunky_7urn1p5}__
