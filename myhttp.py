#!/usr/bin/env python

import sys
import urllib, urllib2
import httplib
import ssl
import cookielib
import socket

GOOGLE="https://www.google.com"
DEFAULTTIMEOUT = 10
# Set to 1 so we won't try repeatedly and get banned
MAXOPENTRIES = 1
# Pass custom UA via MyHTTP(my_user_agent)
# USERAGENT= "curl/7.26.0 (x86_64-pc-linux-gnu) libcurl/7.26.0 OpenSSL/1.0.1e zlib/1.2.7 libidn/1.25 libssh2/1.4.2"
USERAGENT= "python-urllib/2.7 (compatible; biticker/1.0; +http://cr.yptoco.in)"

########################################################################################################
# (OLD) Force Python to use SSLv3: http://bugs.python.org/issue11220#msg128686
# Force Python to use specific protocol (TLS).  The old SSL versions are broken.     -- meb 2014/10/23
########################################################################################################
class HTTPSConnectionTLS(httplib.HTTPSConnection):
    def __init__(self, *args, **kwargs):
        httplib.HTTPSConnection.__init__(self, *args, **kwargs)
        
    def connect(self):
        sock = socket.create_connection((self.host, self.port), self.timeout)
        if self._tunnel_host:
            self.sock = sock
            self._tunnel()
        try:
            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_TLSv1)
        except ssl.SSLError, e:
            raise("Can't establish secure SSL connection")
            
class HTTPSHandlerTLS(urllib2.HTTPSHandler):
    def https_open(self, req):
        return self.do_open(HTTPSConnectionTLS, req)

class MyHTTP:
	"""Organize all the methods used to get a page here"""
	def __init__(self, ua = None):
		self.errcode = 0
		self.errmsg = ''
		self.pagecode = 0
		self.pagetext = ''
		self.ua = ua
		self.cookiejar = cookielib.CookieJar()
		socket.setdefaulttimeout(DEFAULTTIMEOUT)

	def get(self, url = GOOGLE, data = None):
		"""Generic method to handle the URL opening and returning of the page text"""
		pagetext = None
		self.opentries = 0
		if (self.ua):
			headers = {'User-Agent': self.ua, 'Accept' : "application/json"}
		else:
			headers = {'User-Agent': USERAGENT, 'Accept' : "application/json"}

		# opener = urllib2.build_opener(self.cookiejar, urllib2.HTTPSHandler(debuglevel=1))
		# urllib2.install_opener(urllib2.build_opener(HTTPSHandlerV3()))
		## opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookiejar), urllib2.HTTPSHandlerV3(debuglevel=1))
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookiejar), HTTPSHandlerTLS())
		if data:
			edata = urllib.urlencode(data)
			req = urllib2.Request(url, edata, headers)
		else:
			req = urllib2.Request(url, None, headers)
		rez = None

		while(self.opentries < MAXOPENTRIES):
			self.opentries = self.opentries + 1
			# DEBUGGING
			# print "Open attempt " + str(self.opentries) + " on " + url + " with " + repr(data)
			# time.sleep(random.uniform(0,.9))
			try:
				rez = opener.open(req)
			except urllib2.HTTPError, e:
				self.errcode = e.code
				self.errmsg = "HTTP Error"
				continue
			except urllib2.URLError, e:
				self.errcode = e.reason[0]
				#self.errmsg = e.reason[1]
				continue
			except ssl.SSLError:
				self.errcode = 1
				self.errmsg = "SSL connection timed out"
				continue
			try:
				pagetext = rez.read()
			except AttributeError, e:
				self.errcode = 1
				self.errmsg = "No page text returned"
				continue
			if pagetext:
				break
		if rez is None:
			self.errcode = 1
			self.errmsg = "Unable to get URL" 
			return ""

		self.pagecode = rez.getcode()
		self.pagetext = pagetext
		
		# DEBUGGING
		# print "(%d) Pagetext = %s" % (self.pagecode, self.pagetext)
		
		return pagetext

if __name__ == "__main__":
	mhttp = MyHTTP()
	print mhttp.get()
	print mhttp.pagecode
	print mhttp.errcode
	print mhttp.errmsg
