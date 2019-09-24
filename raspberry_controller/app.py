#!flask/bin/python
from threading import Thread

import serial
from flask import Flask, jsonify, send_file, Response
import logging
from logging import Formatter, FileHandler
import os
from picamera import PiCamera

app = Flask(__name__)
camera = PiCamera()
camera.resolution = (1920, 1080)
camera.start_preview()

class DetectionThread(Thread):
    def __init__(self, start_event):
        super(DetectionThread, self).__init__(start_event)
        self.start_event = start_event
        self.camera = PiCamera()
        self.camera.resolution = (1920, 1080)
        self.arduino_serial = serial.Serial("/dev/ttyACM0", 9600, timeout=5) #TODO: See if timeout should be lower

    def detection_loop(self):
        while self.start_event.is_set():
            # Begin first stage of detection. Send command to start detection loop to arduino.
            self.arduino_serial.write(bytes('m', 'UTF-8'))

            # Wait for the IR detection to trigger
            detected=False
            while not detected:
                log = self.arduino_serial.readline().decode()
                # TODO: Use function to send log via REST
                if "Detected" in log:
                    break

            # Take a new snapshot
            self.camera.capture('{}/snapshot.jpg'.format(os.getcwd()))

            # Send request for Tensor Flow server to begin processing.

            # Wait for response from Tensor Flow server

            # Perform sorting

@app.route('/')
def index():
    return "Connection Active: Ready to receive commands!"


@app.route('/snapshot')
def snapshot():
    """
    Return a snapshot as a JPEG mimetype
    :return: MIME object
    """
    if os.path.exists('{}/snapshot.jpg'.format(os.getcwd())):
        return send_file('{}/snapshot.jpg'.format(os.getcwd()), mimetype='image/jpg')
    return "No snapshot taken. Please wait for process to run."


@app.route('/detection')
def


@app.errorhandler(500)
def internal_error(error):
    return jsonify(
        msg='A 500 error was detected: {}'.format(error)
    ), 500


@app.errorhandler(404)
def not_found_error(error):
    return jsonify(
        msg='A 404 error was detected: {}'.format(error)
    )


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
