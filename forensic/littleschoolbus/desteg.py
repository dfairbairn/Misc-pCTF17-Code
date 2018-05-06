import os
from scipy import misc
import numpy as np

def desteg_colourchan(image_path="littleschoolbus.bmp", num_lsb=1):
    """ Do the desteganographification on the image colour channel data only.
        Note: does not use a bit offset """

    image = misc.imread(image_path, flatten=0)
    mask = (255 >> (8 - num_lsb)) # to get 00000011 for 2 lsb, etc.
    list_bin = []
    for row in image:
        for col in row:
            for colourchan in col:
                num = colourchan & mask
                # to format appropriately for 2 bits we would do format(num, "02b") to get e.g. "11"
                # this will end up being "02b", "03b", etc. depending on num_lsb
                num_digits = format(num_lsb, "02") + "b"
                list_bin.append(format(num, num_digits))

    if (num_lsb in [1,2,4]):
        byte_lst = []
        for i in np.arange(len(list_bin)/4):
            bytesum = ""
            for j in range(int(8/num_lsb)):
                if (4*i + j) < len(list_bin):
                    bytesum += list_bin[4*i + j]
            byte_lst.append(bytesum)
    else:
        print("That's all for now, folks")
        byte_lst = None
    return list_bin, byte_lst

def bl2chars(byte_lst):
    """ Takes a list of 8-character strings representing byte data, converts
    to characters if possible. """
    char_inds = []
    chars = []
    for i,byte in enumerate(byte_lst):
        if (int(byte, 2) < 127 and int(byte, 2) > 33):
            char_inds.append(i)
            chars.append(chr(int(byte, 2)))
    return char_inds, chars

def desteg_binary(filename="littleschoolbus.bmp", bit_offset=0):
    """ Only written to do nuM_lsb=1 desteganography """
    try:
        with open(filename, "rb") as f:
            data = f.read()
            data = data[bit_offset:]
            bitlist = []
            for c in data:
                bitlist.append(ord(c) & 1)
            bytelst = []
            for i in range(len(bitlist)/8):
                if (8*i + 7) < len(bitlist):
                    byte = ""
                    for j in range(8):
                        byte += str(bitlist[8*i + j])
                    bytelst.append(byte)
            return bytelst
    except Exception as e:
        print("Exception: {0}".format(e))
    return None

if __name__=="__main__":
    # loop through the possible bit offsets at which the steganography could've been applied
    for i in range(8):
        byte_lst = desteg_binary(bit_offset=i)
        char_inds, chars = bl2chars(byte_lst)
        m = reduce(lambda x,y: x+y, chars)
        if "flag" in m: # In general, this could just look for words from a small dictionary list
            break

    # undoing steganography if only applied to image colour channel data
    #list_bin, byte_lst = desteg_colourchan()
    #char_inds, chas = bl2chars(byte_lst)
