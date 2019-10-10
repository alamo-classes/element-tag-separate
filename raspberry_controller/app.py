#!flask/bin/python
import sys
from threading import Thread, Event
from time import sleep

import json

import requests
import serial
from flask import Flask, jsonify, request
import logging
from logging import Formatter, FileHandler
import os
from flask_cors import CORS

# Create/set the stop event.
STOP_EVENT = Event()
app = Flask(__name__)
CORS(app)  # TODO: Look into making this only work from host origin


class DetectionThread(Thread):
    def __init__(self, stop_event, sorting, label, origin, group=None):
        super(DetectionThread, self).__init__(group, stop_event, sorting, label, origin)
        self.stop_event = stop_event
        self.sorting = sorting
        self.label = label
        self.arduino_serial = serial.Serial("/dev/ttyACM0", 9600, timeout=5)
        self.url = origin

    def run(self):
        print("Starting thread with label: {}".format(self.label), file=sys.stderr)
        # Begin first stage of detection. Send command to start detection loop to arduino.
        self.arduino_serial.write(bytes('a', 'UTF-8'))
        print("Starting arduino servos. Entering detection mode...", file=sys.stderr)
        while not self.stop_event.is_set():
            # Wait for the IR detection to trigger
            detected = False
            while not detected:
                try:
                    log = self.arduino_serial.readline().decode()
                    if "Detected" in log:
                        print("Detection alert triggered", file=sys.stderr)
                        detected = True
                except serial.SerialException:
                    print("Serial Exception found", file=sys.stderr)
                    # TODO: Look into disabling GETTY after demo
                    self.arduino_serial.flush()
                    detected = True

            # Send request for Tensor Flow server to get sorting . Wait for response.
            if self.sorting:
                position = requests.get(url="{}{}/".format(self.url, self.label))
                # Send part through sorter in training position
                print("Sorting received position #{}".format(position.text), file=sys.stderr)
                self.arduino_serial.write(bytes(position.text, 'UTF-8'))
                # Sleep 2 seconds and then continue loop
                sleep(2)
                self.arduino_serial.write(bytes('a', 'UTF-8'))
            # Send request for Tensor Flow to capture an image for processing
            elif not self.sorting and not self.stop_event.is_set:
                requests.get(url="{}{}/".format(self.url, self.label))
                self.arduino_serial.write(bytes)


@app.route('/')
def index():
    return "Connection Active: Ready to receive commands!"


@app.route('/detection_training')
def detection_training():
    """ Start the training detection loop """
    label = request.args.get("label")
    origin = "http://192.168.0.12:8000/capture/detection_training"
    thread = DetectionThread(STOP_EVENT, sorting=False, label=label, origin=origin)
    thread.daemon = True
    thread.start()
    STOP_EVENT.clear()
    return json.dumps({'success': True}), 200


@app.route('/detection_sorting')
def detection_sorting():
    """ Start the sorting detection loop """
    label = request.args.get("profile")
    origin = "http://192.168.0.12:8000/sorting/detection_sorting/"
    thread = DetectionThread(STOP_EVENT, sorting=True, label=label, origin=origin)
    thread.daemon = True
    thread.start()
    STOP_EVENT.clear()
    return "Detection loop started for sorting. Beginning detection loop", 200


@app.route('/stop_detection')
def stop_detection():
    """ Stop the detection loop """
    STOP_EVENT.set()
    return "Detection loop stopping. Wait for loop to finish.", 200


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
