from flask import Flask, request, jsonify, render_template
from beacons import BeaconHeaders

app = Flask(__name__)

# Some logging
if not app.debug:
	import logging
	from logging.handlers import RotatingFileHandler
	fh = RotatingFileHandler('beacon-info.log', maxBytes=100000, backupCount=5)
	fh.setLevel(logging.INFO)
	fh.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s '))
	app.logger.addHandler(fh)

@app.route("/api")
@app.route("/")
def index():
	# rh = request.headers
	# print repr(rh)

	# Process the headers
	bh = BeaconHeaders(request.headers)

	# Put everything into simple data structure for template display
	data = { 'ip' : request.remote_addr,
			'useragent' : bh.useragent,
			'dnt' : bh.dnt,
			'tracked' : bh.track,
			'beacons' : bh.values,
			}

	# Log the header keys only
	if (bh.track):
		app.logger.info('%s %s', request.remote_addr, repr(bh.data.keys()))

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
