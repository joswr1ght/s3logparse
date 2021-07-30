#!/usr/bin/env python3

# Extract useful information from S3 logs. Some of this can be done in awk, but
# the use of quoted strings in the S3 logs makes it difficult to reference some
# fields.

import sys
import shlex

# This is maps the function specified by the user to the Python handler function
parsefuncs = {
        "useragent":"parseuseragent",
        "toptalkers":"parsetoptalkers",
        "topuploaders":"parsetopuploaders",
        "topdownloaders":"parsetopdownloaders",
        "topfiles":"parsetopfiles",
        }

# Get a list of IPs where multiple user agents are used for the same host
#def parseuseragentmulti(logfilelines):

# These are the functions to _do things_ with the S3 log data
def parseuseragent(logfilelines):
    # Get the user agent from each line in the specified log files, making a unique count of each
    useragents = {}
    for line in logfilelines:
        ua = shlex.split(line)[17]
        if ua == "-":
            continue
        if ua not in useragents:
            useragents[ua] = 1
        else:
            useragents[ua] += 1
    sorteduseragents = {k: v for k, v in sorted(useragents.items(), key=lambda item: item[1], reverse=True)}
    for key, value in sorteduseragents.items():
        print(f"{value} - {key}")

def parsetoptalkers(logfilelines):
    # Build a dictionary of unique source IPs and track total transferred bytes
    talkers = {}
    for line in logfilelines:
        el = shlex.split(line)
        sourceip = el[4]
        bytessent = el[12]
        if (bytessent.isnumeric()):
            if sourceip not in talkers:
                talkers[sourceip] = int(bytessent)
            else:
                talkers[sourceip] += int(bytessent)
    sortedtalkers = {k: v for k, v in sorted(talkers.items(), key=lambda item: item[1], reverse=True)}
    for key, value in sortedtalkers.items():
        print(f"{humanreadablesize(value)} - {key}")

def parsetopdownloaders(logfilelines):
    # Build a dictionary of unique source IPs and track total transferred bytes
    talkers = {}
    for line in logfilelines:
        el = shlex.split(line)
        sourceip = el[4]
        request = el[9]
        bytessent = el[12]
        if (bytessent.isnumeric() and request[0:3] == "GET"):
            if sourceip not in talkers:
                talkers[sourceip] = int(bytessent)
            else:
                talkers[sourceip] += int(bytessent)
    sortedtalkers = {k: v for k, v in sorted(talkers.items(), key=lambda item: item[1], reverse=True)}
    for key, value in sortedtalkers.items():
        print(f"{humanreadablesize(value)} - {key}")

def parsetopuploaders(logfilelines):
    # Build a dictionary of unique source IPs and track total transferred bytes
    talkers = {}
    for line in logfilelines:
        el = shlex.split(line)
        sourceip = el[4]
        request = el[9]
        bytessent = el[12]
        if (bytessent.isnumeric() and request[0:4] == "POST"):
            if sourceip not in talkers:
                talkers[sourceip] = int(bytessent)
            else:
                talkers[sourceip] += int(bytessent)
    sortedtalkers = {k: v for k, v in sorted(talkers.items(), key=lambda item: item[1], reverse=True)}
    for key, value in sortedtalkers.items():
        print(f"{humanreadablesize(value)} - {key}")

def parsetopfiles(logfilelines):
    # Build a dictionary of unique source IPs and track total transferred bytes
    files = {}
    for line in logfilelines:
        el = line.split()
        requestfile = el[8]
        if (requestfile == "-"): # Not a file access operation
            continue
        if requestfile not in files:
            files[requestfile] = 1
        else:
            files[requestfile] += 1
    sortedfiles = {k: v for k, v in sorted(files.items(), key=lambda item: item[1], reverse=True)}
    for key, value in sortedfiles.items():
        print(f"{value} - {key}")


# https://stackoverflow.com/a/43690506
# Mebibytes = 2^20 or 1,048,576 bytes.
def humanreadablesize(size, decimal_places=2):
    for unit in ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB']:
        if size < 1024.0 or unit == 'PiB':
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"

if __name__ == "__main__":
    if (len(sys.argv) < 3):
        print("s3logparse.py: Extract useful information from AWS S3 logs.")
        print(f"Usage: {sys.argv[0]} [{'|'.join(parsefuncs.keys())}] <log files>")
        sys.exit(0)

    parsefunc = sys.argv[1]
    logfiles = sys.argv[2:]

    if (parsefunc not in parsefuncs.keys()):
        print(f"Unsupported request function {parsefunc}.")
        sys.exit(1)

    # Open files, read all lines as array
    logfilelines=[]
    for logfile in logfiles:
        try:
            with open(logfile) as f:
                logfilelines += f.readlines()
        except Exception as e:
            print("Unexpected error: ", sys.exc_info()[0])

    locals()[parsefuncs[parsefunc]](logfilelines)
