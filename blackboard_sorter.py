#!/usr/bin/env python3

import errno
import zipfile
from collections import defaultdict
import os
import os.path
import re

netid_re = re.compile(r"[a-z]{3}[0-9]{6}")
txt_re = re.compile(r".*\.txt")
zip_re = re.compile(r".*\.zip")
name_re = re.compile(r"Name: ([a-zA-Z\- ]*) .*")

def getname(files):
    # Get txt files
    txt_files = [f for f in files if txt_re.match(f) is not None]

    name = None
    # Read file
    for txt in txt_files:
        with open(txt, errors='ignore') as f:
            for line in f:
                m = name_re.match(line)
                if m is not None:
                    name = m.group(1)
                    break
        if name is not None:
            break

    return name


def unzip(files, target):
    # Get zip files
    zip_files = [f for f in files if zip_re.match(f) is not None]

    for zip_file in zip_files:
        with zipfile.ZipFile(zip_file) as zfile:
            zfile.extractall(target)


def main():
    all_netid = dict()

    # Build netid dict
    for filename in os.listdir(os.curdir):
        result = netid_re.search(filename)
        if result is None:
            continue
        netid = result.group(0)

        if netid in all_netid:
            all_netid[netid].append(filename)
        else:
            all_netid[netid] = [filename]

    for netid, files in all_netid.items():
        subdir = getname(files)
        # Create folder named netid
        try:
            #os.mkdir(netid)
            os.mkdir(subdir)
        except OSError as err:
            if err.errno != errno.EEXIST:
                raise err

        # Unzip if necceesary
        unzip(files, subdir)

        # move all related files to that folder
        for filename in files:
            if os.path.isfile(filename):
                os.rename(filename, os.path.join(subdir, filename))

if __name__ == "__main__":
    main()
