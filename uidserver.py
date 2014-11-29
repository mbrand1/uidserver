from flask import Flask, request, json, jsonify, render_template
from beacons import BeaconHeaders
from myhttp import MyHTTP

import time

app = Flask(__name__)

def getNetRef(ip = None):
	ARINURL = 'http://whois.arin.net/rest/nets;q='+ip+'?showDetails=false&showARIN=false&ext=netref2'
	http = MyHTTP()
	arindata = json.loads(http.get(ARINURL))
	try:
		owner = arindata['nets']['ns3:netRef']['orgRef']['@name']
	except TypeError:
		owner = arindata['nets']['ns3:netRef'][0]['orgRef']['@name'] # ns3:netRef might be list. Take first ele.
	return owner
	
@app.route("/api")
@app.route("/")
def index():
	# rh = request.headers
	# print repr(rh)
	ipowner = getNetRef(request.remote_addr) 

	# Process the headers
	bh = BeaconHeaders(request.headers)

	# Put everything into simple data structure for template display
	data = { 'ip' : request.remote_addr,
			'ipowner' : ipowner,
			'useragent' : bh.useragent,
			'dnt' : bh.dnt,
			'tracked' : bh.track,
			'beacons' : bh.values,
			}

	# Log the header keys only
	if (bh.track):
		# I still can't get Flask logging to work in production under Apache, so...
		fh = open('/home/netsville/uid/beacon-info.log','a')
		fhout = "{} {}: {}\n".format(time.asctime(), request.remote_addr, repr(bh.data.keys()))
		fh.write(fhout)
		fh.close()

	# See if the API path was hit -- if so, send JSON instead of a page
	if (request.path == '/api'):
		# Add the specific beacons to data
		# Render as JSON
		data.update(bh.data)
		return jsonify(data)
	else:
		# Render as HTML page
		return render_template('uid.html', data=data)

if __name__ == "__main__":
	'''Must run on port 80 if you want to catch real UID tracking headers'''
	app.debug = True
	app.run(host='0.0.0.0',port=8080)
