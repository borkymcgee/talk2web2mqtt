#!/usr/bin/env python3

#url to set in app: "http://192.168.0.17/?text=" + text.replace("/ /g", "~")

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import subprocess
import re

broker="0.0.0.0" #replace with the IP address of your mqtt broker
username = "USERNAME" #replace with your mqtt username
password = "junqtt" #replace with your mqtt password
topic = "pebble/stt" #replace with the topic you want to publish to
http_port = 8080

class S(BaseHTTPRequestHandler):

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
    def do_GET(self):
        message = parse_qs(urlparse(self.path).query)["text"][0].replace("~", " ").lower()
        #strip punctuation
        message = re.sub('[^A-Za-z0-9]+', ' ', message)
        self._set_response()
        print("text recieved: ", message)
        subprocess.call("mosquitto_pub -h {} -t '{}' -m '{}' -u {} -P {} -q 2".format(broker, topic, message, username, password), shell=True)

def run(server_class=HTTPServer, handler_class=S):

    server_address = ('', http_port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('Stopping httpd...\n')

if __name__ == '__main__':
    run()
