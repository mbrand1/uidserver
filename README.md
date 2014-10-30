# uidserver

A Flask app that looks for tracking beacons and displays them to screen

## Installation

I'm on Debian Linux, so...

1. apt-get install python-flask
2. cd to uid directory
3. python ./uidserver.py

This will start up the application on your local machine on port 8080 (for testing).

In order to make this work "for real", you'll need a webserver that can deploy <a href="http://wsgi.readthedocs.org/en/latest/">WSGI</a> apps. See: http://flask.pocoo.org/docs/0.10/deploying/

This application *must* run on port 80.  Otherwise, you won't see any tracking beacons.  They are only injected with normal HTTP requests.

## Licenses

The MIT License (MIT)

Copyright (c) 2014 Micah Brandon &lt;brandon@netsville.com&gt;

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
