"""
file: randomseed_break.py
description:
    Wrote this little bit of code to decrypt a string whose encryption was derived
    from a known seed using python's "random" library. 

    The encryptiono method (below) takes random numbers from 0 to 26 or 0 to 10 and
    performs a cyclic permutation of lowercase/uppercase/numerical alphanumeric 
    characters.

    This was written in order to solve the "Level 1: SoRandom" challenge for PicoCTF 
    2017.
author: David Fairbairn
date: May 2018

"""

import random

def encrypt(c):
  if c.islower():
    #rotate number around alphabet a random amount
    encflag = chr((ord(c)-ord('a')+random.randrange(0,26))%26 + ord('a'))
  elif c.isupper():
    encflag = chr((ord(c)-ord('A')+random.randrange(0,26))%26 + ord('A'))
  elif c.isdigit():
    encflag = chr((ord(c)-ord('0')+random.randrange(0,10))%10 + ord('0'))
  else:
    encflag = c
  return encflag

def decrypt(string, seed_state="random"):
    """
    Decrypts a string encrypted using the above cyclic 'encrypt' method by using the known 
    Seed state that the encryption was initialized with.
    """
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    keys = [] # list of lists
    decrypted = ""
    for char in string:
        key = list()
        if char not in chars:
            print("Passing a non alphanumeric character...")
            decrypted += char
            pass # To deal with the pesky little ':' in the example string
        for letter in chars:
            random.seed(seed_state)
            for c in decrypted:
                encrypt(c) # To progress the random seed state identically
            key.append(encrypt(letter))
            # if not done yet, check if the most recent encryption matches the next character to decrypt
            if len(string) > len(decrypted) and key[-1] == string[len(decrypted)]: 
                decrypted += letter
                print("Decrypted a character! {0}->{1}".format(string[len(decrypted) - 1], letter))
        keys.append(key)
    return decrypted

if __name__=="__main__":
    import sys

    # Took this from running the SoRandom executable on shell2017.picoctf.com (37968)
    encflag = "BNZQ:jn0y1313td7975784y0361tp3xou1g44"

    flag = decrypt(encflag)
    print("Decrypted string: {0}".format(flag))
