import numpy as np


def search_file_bytes(filename, search_bytes):

    try:
        f = open(filename, 'rb')
        data = f.read()
        locations = []
        for i, byte in enumerate(data):
            if (i + len(search_bytes)) < len(data):
                for j in range(len(search_bytes)):
                    #print(ord(data[i + j]))
                    if (ord(data[i + j]) != search_bytes[j]):
                        break
                    else:
                        #print("Looking good so far at location {0}...".format(i))
                        if j == (len(search_bytes) - 1):
                            # Then we found a ting
                            print("Found the search byte! Location: {0}".format(i))
                            locations.append(i)
        f.close()
    except Exception as e:
        print("Exception while opening file and doing things: {0}".format(e))
        locations = None
    return locations

def save_filesegment(in_filename, out_filename, byte_ind_start, byte_ind_end):
    try:
        f = open(in_filename, 'rb')
        data = f.read()
        with open(out_filename, 'wb') as fo:
            fo.write(data[byte_ind_start:byte_ind_end])

        f.close()
    except Exception as e:
        print("Exception while opening file and trying to write a segment from it to another file: {0}".format(e))


#-----------------------------------------------------------------------------
#                         Filesignature search
#-----------------------------------------------------------------------------

def find_archive_signatures(fname):
    """ Takes fname and looks for signatures for archive filetypes within it """
    print("Looking for tar zip files zipped with Lempel-Ziv-Welch...(note, this signature is pretty short and easy to find by accident)")
    search_bytes = [int("1f",16), int("9d",16)]
    locations = search_file_bytes(fname, search_bytes)

    print("Looking for tar zip files zipped using LZH...(note, this signature is pretty short and easy to find by accident)")
    search_bytes = [int("1f",16), int("a0",16)]
    locations = search_file_bytes(fname, search_bytes)

    print("Looking for gunzip archives...(note, this signature is pretty short and easy to find by accident)")
    search_bytes = [int("1f",16), int("8b",16)]
    locations = search_file_bytes(fname, search_bytes)

    print("Looking for 7zip archives ... ")
    search_bytes = [int("37",16), int("7a",16), int("bc",16), int("af", 16), int("27", 16), int("1c", 16)]
    locations = search_file_bytes(fname, search_bytes)

    print("Looking for RAR archives ... ")
    search_bytes = [int("52",16), int("61",16), int("72",16), int("21", 16), int("1a", 16), int("07", 16)]
    locations = search_file_bytes(fname, search_bytes)

    print("Looking for tar archives ... ")
    search_bytes = [int("75",16), int("73",16), int("74",16), int("61", 16), int("72", 16)]
    locations = search_file_bytes(fname, search_bytes)

def find_executable_signatures(fname):
    print("Looking for ELF files... ")
    search_bytes = [int("7f",16), int("45",16), int("4c",16), int("46", 16)]
    locations = search_file_bytes(fname, search_bytes)

    print("Looking for .exe files... (note, this signature is pretty short and easy to find by accident)")
    search_bytes = [int("4d",16), int("5a",16)]
    locations = search_file_bytes(fname, search_bytes)


def find_media_signatures(fname):
    print("Looking for jpegs ... ")
    search_bytes = [int("ff",16), int("d8",16), int("ff",16)]
    locations = search_file_bytes(fname, search_bytes)

    print("Looking for PNG files ... ")
    search_bytes = [int("89",16), int("50",16), int("4e",16), int("47", 16), int("0d", 16), int("0a", 16), int("1a", 16), int("0a",16)]
    locations = search_file_bytes(fname, search_bytes)

    print("Looking for wav files ... ")
    search_bytes = [int("52",16), int("49",16), int("46",16), int("46", 16)]
    locations = search_file_bytes(fname, search_bytes)




if __name__=="__main__":
    fname = "file"
    #search_bytes = [137, 80, 78, 71, 13, 10, 26, 10]

    find_archive_signatures(fname)
    find_executable_signatures(fname)
    find_media_signatures(fname)

    """
    with open(fname, 'rb') as f:
        flen = len(f.read())
    for i,start_ind in enumerate(locations):
        if start_ind != locations[-1]:
            save_filesegment(fname, "f{0}.png".format(i), start_ind, locations[i+1] - 1)
        else:
            save_filesegment(fname, "f{0}.png".format(i), start_ind, flen)
    """
