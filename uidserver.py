from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

@app.route("/<otype>")
@app.route("/")
def showheaders(otype=None):
	rh = request.headers

	# Beacons for testing: uncomment these to force a tracking beacon through
	testbeacons = {
#					'x-uidh' : "da89f98sfiasdfw-lh2345h2kj34h23k2234j2k3ljr289asfasdfasdfkasd--fas9f0asdfas",
#					'x-acr' : "ASDHFASDFAS89DFASDFASDJKFSF0WKJWFKWE-JASDKFASFASDFADFA-ASDFASDFKASDFJAKLSDJFLAKSDFJASKDJFAKDFA",
					} 

	# Check for beacons
	beacons = []
	track = False
	if rh.get('X-UIDH'):
		beacons.append(rh.get('X-UIDH'))
		track = True
	if rh.get('X-ACR'):
		beacons.append(rh.get('X-ACR'))
		track = True
	for k, v in testbeacons.items():
		if k == 'x-uidh':
			beacons.append(v)
			track = True
		if k == 'x-acr':
			beacons.append(v)
			track = True

	# Check do-not-track setting
	Dnt = 'Disabled'
	if rh.get('Dnt'):
		Dnt = 'Enabled'

	# Put everything into simple data structure for template display
	data = { 'ip' : request.remote_addr,
			'useragent' : rh.get('User-Agent'),
			'dnt' : Dnt,
			'tracked' : track,
			'beacons' : beacons,
			'uidh' : rh.get('X-UIDH'),
			'acr' : rh.get('X-ACR'),
			}		

	# Check output type (otype) for how to return data
	if (otype == 'json'):
		# Render as JSON
		return jsonify(data)
	else:
		# Render as HTML page
		return render_template('uid.html', data=data)

if __name__ == "__main__":
	'''Must run on port 80 if you want to catch real UID tracking headers'''
	app.debug = True
	app.run(host='0.0.0.0',port=8080)
