#!/usr/bin/env python

from boto.s3.connection import S3Connection
from boto.s3.key import Key
from creds import *
from uuid import uuid4
from os import environ

environ['PYTHONUNBUFFERED'] = '1'

class DataGenerator:

    def __init__(self, size):
        self.size = size
        self.pos = 0
        self.fp = open('/dev/urandom', 'rb')

    def __del__(self):
        self.fp.close()
    
    def tell(self):
        print 'tell: %d' % self.pos
        return self.pos

    def seek(self, pos, whence=0):
        print 'seek: %d (%d)' % (pos, whence)
        if whence == 0:
            self.pos = pos
        elif whence == 1:
            self.pos += pos
        elif whence == 2:
            self.pos = self.size
        else:
            raise IOException('unsupported whence: %d' % whence)

    def read(self, size=None):
        if self.pos + size > self.size:
            size = self.size - self.pos
        ret = self.fp.read(size)
        self.pos += len(ret)
        return ret


def progress(up, tot):
    print '    {0} of {1}'.format(up, tot)


conn = S3Connection(KEY, SECRET)
bucket = conn.get_bucket(BUCKET)
key = Key(bucket)
for size in (1,):
    key.key = '{0:04d}'.format(size)
    fp = DataGenerator(size)
    print 'uploading {0} MB file'.format(size)
    key.set_contents_from_file(fp, policy='public-read', cb=progress,
                               num_cb=100)
