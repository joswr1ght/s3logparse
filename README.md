# s3logparse.py - A Simple Parser for AWS S3 Logs

[![Python application](https://github.com/joswr1ght/s3logparse/actions/workflows/python-app.yml/badge.svg)](https://github.com/joswr1ght/s3logparse/actions/workflows/python-app.yml)
> Joshua Wright | [josh@willhackforsushi.com](mailto:josh@willhackforsushi.com)

Sure, you could use CloudWatch, but sometimes you just want to grab some
stats at the command line.

## Usage

First, grab your S3 logs to a directory on the file system:

```
$ mkdir mys3logs && cd mys3logs
$ aws s3 cp s3://your-s3-logging-bucket . --recursive
$ cd ..
```

Then download this script and run it:

```
$ git clone https://github.com/joswr1ght/s3logparse.git
$ cd s3logparse
$ chmod 755 s3logparse.py
$ ./s3logparse.py
s3logparse.py: Extract useful information from AWS S3 logs.
Usage: ./s3logparse.py [useragent|toptalkers|topuploaders|topdownloaders|topfiles] <log files>
```

## Examples

### Identify Top Talkers

```
$ ./s3logparse.py toptalkers ../mys3logs/*
20.43 GiB - 254.59.11.25
15.95 GiB - 253.252.70.185
13.80 GiB - 252.59.250.11
12.85 GiB - 251.252.12.173
12.81 GiB - 251.252.12.190
...
```

### Identify User Agents

```
$ ./s3logparse.py useragent ../mys3logs/* | cut -c 1-72
34140 - aws-cli/1.16.192 Python/2.7.10 Darwin/18.7.0 botocore/1.12.182
876 - Amazon CloudFront
222 - Cyberduck/7.1.1.31577 (Mac OS X/10.14.6) (x86_64)
69 - S3Console/0.4, aws-internal/3 aws-sdk-java/1.11.915 Linux/4.9.230-0
44 - S3Console/0.4, aws-internal/3 aws-sdk-java/1.11.991 Linux/5.4.109-5
...
```

## Functions

If you want to get some non-trivial information from the logs that you think would be
useful for others please [let me know](mailto:josh@willhackforsushi.com).

### useragent

Identifies the User Agent information for access attempts (successful and
failed). Does not include the empty User Agent `-`.

### toptalkers

Identifies the source IP addresses and bytes transferred cumulative for all
specified log files (combined upload and download). Turns byte counts into
human readable [mebibits](https://en.wikipedia.org/wiki/Mebibit).

### topuploaders

Like `toptalkers`, but only for POST/uploads.

### topdownloaders

Like `toptalkers`, but only for GET/downloads.

### parsetopfiles

Identifies a list of files with a cumulative frequency of uploads and
downloads.

## Tests

```bash
❯ pip3 install -r tests/requirements.txt
...
❯ PYTHONPATH='.' pytest tests -v
======================================================== test session starts ========================================================
platform linux -- Python 3.9.6, pytest-6.2.4, py-1.10.0, pluggy-0.13.1 -- /usr/bin/python
cachedir: .pytest_cache
rootdir: /home/dpendolino/git/s3logparse
plugins: mock-3.1.1
collected 6 items

tests/s3logparse_test.py::test_humanreadablesize PASSED                                                                       [ 16%]
tests/s3logparse_test.py::test_main_toptalkers PASSED                                                                         [ 33%]
tests/s3logparse_test.py::test_main_useragent PASSED                                                                          [ 50%]
tests/s3logparse_test.py::test_main_topuploaders PASSED                                                                       [ 66%]
tests/s3logparse_test.py::test_main_topdownloaders PASSED                                                                     [ 83%]
tests/s3logparse_test.py::test_main_topfiles PASSED                                                                           [100%]

========================================================= 6 passed in 0.02s =========================================================
```

_NOTE:_ Sample logs, `tests/test.log`, taken from https://docs.aws.amazon.com/AmazonS3/latest/userguide/LogFormat.html
