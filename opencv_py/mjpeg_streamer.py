#!/usr/bin/python """ Original Author: Igor Maculan - n3wtron@gmail.com A Simple mjpg stream http server https://gist.github.com/n3wtron/4624820 """ from __future__ import absolute_import
from __future__ import print_function

import argparse
import time

from six.moves.BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from six.moves.socketserver import ThreadingMixIn
import cv2

parser = argparse.ArgumentParser()
parser.add_argument('--global', '-g', action='store_true', help='Bind to 0.0.0.0 instead of localhost')
parser.add_argument('--port', '-p', type=int, default=8080, help='Port to bind to')
parser.add_argument('--verbose', '-v', action='store_true', help='Report every frame sent')
args = parser.parse_args()

capture = None


class CamHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--boundary')
        self.end_headers()
        while True:
            try:
                rc, img = capture.read()
                if not rc:
                    print('Error reading frame!')
                    continue
                status, buffer = cv2.imencode('.jpg', img)
                if not status:
                    print('error encoding frame')
                    break
                self.wfile.write(b'\r\n--boundary\r\n')
                self.send_header('Content-type', 'image/jpeg')
                self.send_header('Content-length', len(buffer))
                self.end_headers()
                self.wfile.write(buffer)
                time.sleep(0.25)
                if args.verbose:
                    print('frame (shape {}) sent'.format(img.shape))
            except KeyboardInterrupt:
                print('keyboard interrupt')
                break


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


def main():
    global capture
    capture = cv2.VideoCapture(0)

    try:
        address = '0.0.0.0' if getattr(args, 'global') else 'localhost'
        server = ThreadedHTTPServer((address, args.port), CamHandler)
        print('server started on {}:{}'.format(address, args.port))
        server.serve_forever()
    except KeyboardInterrupt:
        capture.release()
        server.socket.close()


if __name__ == '__main__':
    main()
