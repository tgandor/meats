#!/usr/bin/env python

"""
Original Author: Igor Maculan - n3wtron@gmail.com
A Simple mjpg stream http server https://gist.github.com/n3wtron/4624820
"""

from __future__ import absolute_import
from __future__ import print_function

import argparse
import time

from six.moves.BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from six.moves.socketserver import ThreadingMixIn
import cv2
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--global', '-g', action='store_true', help='Bind to 0.0.0.0 instead of localhost')
parser.add_argument('--port', '-p', type=int, default=8080, help='Port to bind to')
parser.add_argument('--verbose', '-v', action='store_true', help='Report every frame sent')
parser.add_argument('--delay', '-s', type=float, default=1./30, help='Seconds to sleep between frames')
args = parser.parse_args()

capture = None


class CamHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--boundary')
        self.end_headers()
        counter = 0
        start = time.time()
        while True:
            try:
                rc, img = capture.read()
                if not rc:
                    print('Error reading frame!')
                    continue
                status, buffer = cv2.imencode('.jpg', img)  # type: bool, np.ndarray
                if not status:
                    print('Error encoding frame!')
                    break
                counter += 1
                self.wfile.write(b'\r\n--boundary\r\n')
                self.send_header('Content-type', 'image/jpeg')
                self.send_header('Content-length', len(buffer))
                self.end_headers()
                self.wfile.write(buffer.tostring())
                time.sleep(args.delay)
                if args.verbose:
                    print('[{}] frame {} (shape {}, compressed {:,}) sent'.format(
                        time.time() - start, counter, img.shape, len(buffer)
                    ))
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
