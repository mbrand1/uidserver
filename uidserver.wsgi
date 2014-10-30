# We do not want to install our application system wide, so...
import sys
sys.path.insert(0, '/home/netsville/uid')

from uidserver import app as application

application.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
