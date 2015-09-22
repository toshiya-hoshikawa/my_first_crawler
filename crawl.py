#!/usr/bin/env python

import cStringIO
import formatter
from htmllib import HTMLParser
import httplib
import os
import sys
import urllib
import urlparse

class Retriever(object):
    __slots__ = ('url', 'file')
    def __init__(self, url):
        self.url, self.file = self.get_file(url)

    def get_file(self, url, default='index.html'):
        'Create usable local filename from URL'
        parsed = urlparse.urlparse(url)
        host = parsed.netloc.split('@')[-1].split(':')[0]
        filepath = '%s%s' % (host, parsed.path)
        if not os.path.spiltext(parsed.path)[1]:
            filepath = os.path.join(filepath, default)
        linkdir = os.path.dirname(filepath)
        if not os.path.isdir(linkdir):
            if os.path.exists(linkdir):
                os.unlink(linkdir)
            os.makedirs(linkdir)
        return url, filepath

    def download(self):
        'Download URL to specific named file'
        try:
            retval = urllib.urlretrieve(self.url, self.file)
        except (IOError, httplib.InvalidURL) as e:
            retval = (('*** ERROR: bad URL "%s": %s' % (self.url, e)), )
        return retval

    def parse_links(self):
        'Parse out the links found in downloaded HTML file'
        f = open(self.file, 'r')
        data = f.read()
        f.close()
        parser = HTMLParser(formatter.AbstractFormatter(formatter.DumbWriter(
            cStringIO.StringIO())))
        parser.feed(data)
        parser.close()
        return parser.anchorlist

