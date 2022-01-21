"""
This example shows how to run a basic web server in background.
https://www.itsecguy.com/custom-web-server-responses-with-python/
"""


from http.server import BaseHTTPRequestHandler, HTTPServer
from webbrowser import open
from background import BackgroundTask # For running in background
import notifications as nc 
import threading

# The server request handler
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        
        # Send a notification when a request is made
        notification = nc.Notification()
        notification.message = "Made GET Request"
        nc.schedule_notification(notification, 1, False)

        # Send "Hello World"
        message = "Hello World!"

        self.protocol_version = "HTTP/1.1"
        self.send_response(200)
        self.send_header("Content-Length", len(message))
        self.end_headers()

        self.wfile.write(bytes(message, "utf8"))
        return

class task(threading.Thread):
  def __init__(self,server):
    threading.Thread.__init__(self)
    self.server = server
  def run(self):
    self.server.serve_forever()

# Run the server
def run():
    server = ('', 80)
    httpd = HTTPServer(server, RequestHandler)
    httpd.serve_forever()
    
# Open the localhost in Safari
open("http://localhost")

server = ('', 80)
httpd = HTTPServer(server, RequestHandler)
t = task(httpd)
t.start()

from pyto_ui import Alert
alert = Alert("Hello", "Tap ok to stop webserver")
alert.add_action("Ok")
alert.show()
t.server.shutdown()
    
