from http.server import BaseHTTPRequestHandler, HTTPServer
from requests import *
from utils import BasicConfig, __version__
from modules import Handle
import logging


class Webhook(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()


    def do_POST(self):
        self._set_response()
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        Handle().handle(post_data, self.path)


def run(server_class=HTTPServer, handler_class=Webhook, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)
    logging.info("="*100)
    logging.info("Vngitbot {} has started on {}:{}".format(__version__, addr, port))
    httpd.serve_forever()

if __name__ == "__main__":
    bc = BasicConfig()
    bc.logConfig()

    # Declare Endpoint information
    endpointAddress = bc.parser.get('ENDPOINT', 'ENDPOINT_ADDRESS')
    endpointPort = bc.parser.get('ENDPOINT', 'ENDPOINT_PORT')

    # Run Webhook Endpoint
    run(addr=endpointAddress, port=int(endpointPort))
