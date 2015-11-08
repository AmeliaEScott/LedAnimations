import time
import thread
import json
import BaseHTTPServer
from animations.stars import Stars
from animations.staticlight import StaticLight
from animations.fire import Fire
from animations.strobe import Strobe
from animations.fairy import Fairy
from leds import Leds
from urlparse import urlparse, parse_qs

HOST_NAME = '192.168.0.50'
PORT_NUMBER = 8080 # Maybe set this to 9000.


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    
    leds = Leds()
    thread.start_new_thread(leds.run, ())
    
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        data = parse_qs(urlparse(s.path).query)
        #print data
        print "stuff"
        
        if s.path.startswith('/getanimations'):
            print "stuff pt2"
            s.send_response(200)
            s.send_header("Content-type", "application/json");
            s.end_headers()
            s.wfile.write("[")
            for anim in s.leds.animations:
                s.wfile.write(anim.toJson())
                s.wfile.write(", ")
            s.wfile.write("]")
            #s.wfile.write(json.dumps(s.leds.animations))
        elif s.path.startswith('/addanimation'):
            #print data['animation']
            #print data['maxStandDev'][0]
            if data['animation'][0] == 'fire':
                s.leds.add(Fire(s.leds.strip, float(data['maxBrightness'][0]), int(data['center'][0]),
                    float(data['minStandDev'][0]), float(data['maxStandDev'][0])))
            elif data['animation'][0] == 'stars':
                s.leds.add(Stars(s.leds.strip, int(data['starCount'][0]), float(data['brightness'][0]),
                    int(data['red'][0]), int(data['green'][0]), int(data['blue'][0])))
            elif data['animation'][0] == 'fairy':
                s.leds.add(Fairy(s.leds.strip, int(data['start'][0]), float(data['width'][0]), float(data['speed'][0]),
                    int(data['red'][0]), int(data['green'][0]), int(data['blue'][0])))
            elif data['animation'][0] == 'staticlight':
                s.leds.add(StaticLight(s.leds.strip, int(data['start'][0]), int(data['end'][0]),
                    int(data['red'][0]), int(data['green'][0]), int(data['blue'][0])))
            elif data['animation'][0] == 'strobe':
                s.leds.add(Strobe(s.leds.strip, int(data['start'][0]), int(data['end'][0]), int(data['on'][0]), int(data['off'][0]),
                    int(data['red'][0]), int(data['green'][0]), int(data['blue'][0])))
        #if data.has_key('id'):
        #        print data['id'][0]
        #        if s.path.startswith('/animation'):
        #                print 'YYYAAAAAAAAAASSSSS'
        #        else:
        #                print 'NNNAAAAAAAAAAHHHHHH'
        #s.send_response(200)
        #s.send_header("Content-type", "text/html")
        #s.end_headers()
        #s.wfile.write("<html><head><title>Title goes here.</title></head>")
        #s.wfile.write("<body><p>This is a test.</p>")
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        #s.wfile.write("<p>You accessed path: %s</p>" % s.path)
        #s.wfile.write("</body></html>")
