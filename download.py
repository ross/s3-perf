#!/usr/bin/env python

from boto.s3.connection import S3Connection
from boto.s3.key import Key
from creds import *
from datetime import datetime
from os import environ

environ['PYTHONUNBUFFERED'] = '1'

conn = S3Connection(KEY, SECRET)
bucket = conn.get_bucket(BUCKET)
key = Key(bucket)
for size in (1, 10, 100):
    key.key = '{0:04d}'.format(size)
    print 'download {0} MB file'.format(size)
    start = datetime.now()
    key.get_contents_to_filename('/dev/null')
    duration = datetime.now() - start
    duration = (getattr(duration, 'minutes', 0) * 60) + \
        duration.seconds + (duration.microseconds / 1E6)
    print '   took {0:0.2f}s {1:0.2f}MB/s'.format(duration, size / duration)
