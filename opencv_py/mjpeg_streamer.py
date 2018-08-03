#!/usr/bin/python

"""
Original Author: Igor Maculan - n3wtron@gmail.com
A Simple mjpg stream http server
https://gist.github.com/n3wtron/4624820
"""

from __future__ import absolute_import
from __future__ import print_function
import time
from six.moves.BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from six.moves.socketserver import ThreadingMixIn
import cv2

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
                self.wfile.write(b'--boundary\r\n')
                self.send_header('Content-type', 'image/jpeg')
                self.send_header('Content-length', len(buffer))
                self.end_headers()
                self.wfile.write(buffer)
                time.sleep(0.25)
            except KeyboardInterrupt:
                print('keyboard interrupt')
                break
            except ConnectionError:
                print('connection error')
                break


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


def main():
    global capture
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    # why was is B/W?
    # capture.set(cv2.CAP_PROP_SATURATION, 0.2)

    try:
        server = ThreadedHTTPServer(('localhost', 8080), CamHandler)
        print("server started")
        server.serve_forever()
    except KeyboardInterrupt:
        capture.release()
        server.socket.close()


if __name__ == '__main__':
    main()
