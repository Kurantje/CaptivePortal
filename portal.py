from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qsl
import time

import argparse

parser = argparse.ArgumentParser("portal")
parser.add_argument("host", help="The IP address the web server is listening.")
parser.add_argument("port", help="The port the web server is listening.", type=int)
args = parser.parse_args()

class MyServer(BaseHTTPRequestHandler):

    '''
    captive portal html form
    '''
    def html_portal_page(self, ssid):
        html_page = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Hello world!</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body>
            <h1>Set WiFi credentials</h1>
            <form method="POST" action="do_login">
                <p>
                    <label for="id">Enter the network SSID:</label>
                    <input id="id" name="ssid" type="text" value="{ssid}" placeholder="ssid">
                </p>
                <p>
                    <label for="pwd">Enter the password:</label>
                    <input id="pwd" name="password" type="password">
                </p>
                <input type="submit" value="Submit credentials">
            </form>
        </body>
        </html>
        """
        return(html_page)

    '''
    present portal page
    '''
    def do_GET(self):
        print(time.asctime(), "do_GET: Headers=", self.headers)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        '''
        show portal page
        '''
        new_portal_page = self.html_portal_page("")
        self.wfile.write(bytes(new_portal_page, "utf8"))

    '''
    this is called when the user submits the login form
    '''
    def do_POST(self):
        print(time.asctime(), "do_POST: Headers=", self.headers)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        '''
        get form field values
        '''
        length = int(self.headers.get('content-length'))
        field_data = self.rfile.read(length)
        fields = parse_qsl(str(field_data, "UTF-8"))
        print("fields received:", fields)

        '''
        show portal page
        '''
        if 'ssid' in dict(fields).keys():
                new_portal_page = self.html_portal_page(dict(fields)['ssid'])
        else:
                new_portal_page = self.html_portal_page("")
        self.wfile.write(bytes(new_portal_page, "utf8"))

myServer = HTTPServer((args.host, args.port), MyServer)
try:
    print(f"Starting web server on {args.host}:{args.port}")
    myServer.serve_forever()
except KeyboardInterrupt:
    pass
print("Server stopped")
exit(0)
