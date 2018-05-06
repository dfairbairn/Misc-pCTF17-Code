"""
For parsing a .pcap from a USB keyboard device. 

Requirements were pretty minimal as this was for an intro-level CTF problem, so 
there's not much parsing/filtering of packets needed here.

Currently only does the basic alphanumeric characters with usage ID of 0x00 - 0x27.

See here (around page 53) for details on typical keyboard
http://www.usb.org/developers/hidpage/Hut1_12v2.pdf?

Date: May 2018
Author: David Thomas Fairbairn

"""
import scapy
import sys
from scapy.all import rdpcap
import binascii

# How we'll handle the printable-vs-nonprintable chars for now is by using len 1 strings containing
# printable chars for those that can be printed, and just have longer length strings that are 
# checked for when doing other processing
lower = ['RESERVED','KEYB_ROLLOVER_ERR', 'KEYB_POSTFAIL', 'KEYB_ERRUNDEF']

chars_l = lower + [chr(i + ord('a')) for i in range(26)] + ['1','2','3','4','5','6','7','8','9','0']
chars_u = lower + [chr(i + ord('A')) for i in range(26)] + ['!','@','#','$','%','^','&','*','(',')']
chars_l += ['enter','escape','backspace','tab','spacebar','-','=','[',']','\\','NON-US #',';','\'','`',',','.','/']
chars_u += ['enter','escape','backspace','tab','spacebar','_','+','{','}','|', 'NON-US ~',':','"','~','<','>','?']

higher = ['CAPSLOCK','F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12','PRNTSCRN','SCRLLOCK']
higher += ['PAUSE','INSERT','HOME','PAGEUP','DEL','END','PAGEDOWN','RIGHTARROW','LEFTARROW','DOWNARROW','UPARROW'] 
chars_l += higher
chars_u += higher

class KeyboardCapture(object):
    def __init__(self, keycmd_lst=[], pcap_fname=""):
        self.keycmd_lst = keycmd_lst
        self.pcap_fname = pcap_fname

    def parse_pcap(self):
        """
        Fill up object's keycmd_lst with data from file with name self.pcap_fname
        """
        if len(self.keycmd_lst) != 0:
            print("Warning: overwriting the parsed commands already in keycmd_lst.")
        try:
            packets = rdpcap(self.pcap_fname)
            charbytes  = [ binascii.hexlify(str(sd)[-8:]) for sd in packets] 
            self.keycmd_lst = []
            for i in charbytes:
                self.keycmd_lst.append(char_translate(i))
        except Exception as e:
            print("Problem with parsing .pcap: {0}".format(e))

    def __repr__(self):
        for i, keycmd in enumerate(self.keycmd_lst):
            print("{0}:\t{1}".format(i,keycmd))

    def recreate_char_inputs(self):
        out_str = ""
        for keycmd in self.keycmd_lst:
            out_str += keycmd if len(keycmd)==1 else ""
        print(out_str)
       
def char_translate(hexstr):
    output = ""
    if (hexstr[0:2] == "20"):
        # Shift is down
        lookup_dict = chars_u 
    elif (hexstr[0:2] == "00"):
        # Shift is not down
        lookup_dict = chars_l
    elif (hexstr[0:2] == "01"):
        # Control is down?
        lookup_dict = chars_l
        output += "CTRL-"  
    else:
        # Not seen this before. Be noisy.
        print("Strange USB case prefix! {0}".format(hexstr))
        return ""
    usageID = int(hexstr[4:6], 16) 
    if (usageID > len(chars_l)):
        return ""
    else:
        output += lookup_dict[usageID]
    return output

if __name__=="__main__":
    if len(sys.argv) > 1:
        k = KeyboardCapture(pcap_fname=sys.argv[1])
        k.parse_pcap()
        k.recreate_char_inputs()
