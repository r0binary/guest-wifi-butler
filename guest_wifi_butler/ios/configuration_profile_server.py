import os
import atexit
import BaseHTTPServer
import threading
from guest_wifi_butler.ios.http_request_handler import HTTPRequestHandler


class iOSConfigurationProfileServer:
    def __init__(self):
        self.httpd = None
        self.server_thread = None
        atexit.register(self.stopServer)

    def stopServer(self):
        if self.httpd is not None and self.server_thread is not None:
            print('Terminating HTTP server')
            self.httpd.shutdown()
            self.server_thread.join()
            self.httpd = None
            self.server_thread = None

    def startServer(self, address='127.0.0.1', port=5000):
        print('Starting HTTP server on %s:%d' % (address, port))

        self.httpd = BaseHTTPServer.HTTPServer(
            (address, port), HTTPRequestHandler)
        self.server_thread = threading.Thread(
            target=self.httpd.serve_forever, args=())
        self.server_thread.daemon = True
        self.server_thread.start()
