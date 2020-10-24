#!/usr/bin/python3

import sys
from itinerari import link

def usage():
    print("A - B")

if __name__ == "__main__":
    args = sys.argv[1:]
    if '-' not in args:
        usage()
    else:
        [start, end] = " ".join(args).split(' - ')
        print(link(start, end))