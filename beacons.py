#!/usr/bin/env python

# Headers that are used to uniquely id a mobile customer
BEACONS = [
		'X-UIDH',
		'X-ACR',
		'X-VF-ACR',
		'X-UP-SUBNO',
		'X-UP-VODACOMGW-SUBID',
		'X-PIPER-ID',
		'X-MSISDN',
		'X-ATT-DeviceId',
		'X-Wap-Profile',
		'X-JPHONE-UID',
		'X-Nokia-MSISDN',	
		'X-Nokia-Alias',	
		'X-Up-Calling-Line-Id',
		'x-avantgo-userid',
		'x-wsb-identity',
		'x-wte-msisdn',
		'x-imsi',
		'x-h3g-msisdn',
		'x-drutt-portal-user-msisdn',
		'x-drutt-portal-user-id',
		'X-WAP-NETWORK-CLIENT-MSISDN'
	]

class BeaconHeaders:
	""" Determine if any headers passed in are BEACONS """

	def __init__(self, rh):
		self.track = False
		self.data = {}
		self.values = []
		self.dnt = rh.get('Dnt') and 'Enabled' or 'Disabled'
		self.useragent = rh.get('User-Agent')

		for b in BEACONS:
			if rh.get(b):
				self.data[b.lower()] = rh[b]

		if self.data:
			self.track = True
			self.values = self.data.values()

