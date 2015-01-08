#!/usr/bin/env python

import argparse
import hashlib
import os


def summarise(directory):
    '''Returns dictionary keyed by file hash with a value of all matching filenames'''
    files = {}
    for dirname, dirnames, filenames in os.walk(directory):
        for leafname in filenames:
            filename = os.path.join(dirname, leafname)
            filehash = hashlib.sha256(open(filename, "rb").read()).hexdigest()
            files.setdefault(filehash, []).append(filename)
    return files


def diff(directories):
    '''Takes a list of directory names and returns a list of missing files in latter directories''' 
    basefiles = summarise(directories[0])
    originalHash = set(basefiles.keys())

    files = {}
    for dr in directories[1:]:
        files.update(summarise(dr))

    hashes = set(files.keys())
    output = []
    for missing in originalHash - hashes:
        output.append("missing: {}".format(basefiles[missing]))

    return output
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Directory differ")
    parser.add_argument("directories", nargs="+", help="Directories to compare")
    args = parser.parse_args()
    print "\n".join(diff(args.directories))
