#!/usr/bin/env python

from boto.s3.connection import S3Connection
from boto.s3.key import Key
from creds import *
from datetime import datetime
from os import environ
from sys import argv

environ['PYTHONUNBUFFERED'] = '1'

def create_file(size):
    filename = '{0:04d}.meg'.format(size)
    size *= 1024 * 1024
    with open('/dev/urandom', 'rb') as rand:
        with open(filename, 'wb') as fh:
            while size:
                buf = rand.read(size)
                size -= len(buf)
                fh.write(buf)
    return filename

def progress(up, tot):
    print '    {0:0.2f}'.format(up / float(tot))


conn = S3Connection(KEY, SECRET)
bucket = conn.get_bucket(argv[1] if len(argv) > 1 else BUCKET)
key = Key(bucket)
for size in (1, 10, 100):
    key.key = '{0:04d}'.format(size)
    filename = create_file(size)
    print 'uploading {0} MB file'.format(size)
    start = datetime.now()
    key.set_contents_from_filename(filename, policy='public-read',
                                   cb=progress)
    duration = datetime.now() - start
    duration = (getattr(duration, 'minutes', 0) * 60) + \
        duration.seconds + (duration.microseconds / 1E6)
    print '   took {0:0.2f}s {1:0.2f}MB/s'.format(duration, size / duration)
