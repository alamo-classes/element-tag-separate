#!flask/bin/python
import sys
from threading import Thread
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
app = Flask(__name__)
CORS(app)  # TODO: Look into making this only work from host origin

start_event = False
sorting = False
label = ""
url_origin = "127.0.0.1"  # Origin of tensor host


def arduino(url):
    global start_event, sorting, label
    print("Starting thread...", file=sys.stderr)
    app.logger.info("Starting threaded arduino subroutine...")
    arduino_serial = serial.Serial("/dev/ttyACM0", 9600, timeout=5)
    app.logger.info("Arduino connection started")
    while True:
        if start_event:
            # Begin first stage of detection. Send command to start detection loop to arduino.
            arduino_serial.write(bytes('a', 'UTF-8'))
            print("Starting arduino servos. Entering detection mode...", file=sys.stderr)
            app.logger.info("Starting arduino servos. Entering detection mode...")
        while start_event:
            # Wait for the IR detection to trigger
            detected = False
            while not detected:
                log = arduino_serial.readline().decode()
                if "Detected" in log:
                    print("Detection alert triggered", file=sys.stderr)
                    app.logger.info("Part Detected")
                    detected = True

            # Send request for Tensor Flow server to get sorting . Wait for response.
            if sorting:
                position = requests.get(url="http://{}/sorting/detection_sorting/{}/".format(url, label))
                # Send part through sorter in training position
                print("Sorting received position #{}".format(position.text), file=sys.stderr)
                arduino_serial.write(bytes(position.text, 'UTF-8'))
                # Sleep 2 seconds and then continue loop
                sleep(2)
            # Send request for Tensor Flow to capture an image for processing
            else:
                requests.get(url="http://{}/capture/detection_training/{}/".format(url, label))
                print("New photo captured for label: {}".format(label))

            if not start_event:
                arduino_serial.write(bytes('a', 'UTF-8'))


@app.route('/')
def index():
    return "Connection Active: Ready to receive commands!"


@app.route('/detection_training')
def detection_training():
    """ Start the training detection loop """
    global label, sorting, start_event
    label = request.args.get("label")
    sorting = False
    start_event = True
    return json.dumps({'success': True}), 200


@app.route('/detection_sorting')
def detection_sorting():
    """ Start the sorting detection loop """
    global label, start_event, sorting
    label = request.args.get("profile")
    sorting = True
    start_event = True
    return "Detection loop started for sorting. Beginning detection loop", 200


@app.route('/stop_detection')
def stop_detection():
    """ Stop the detection loop """
    global start_event
    start_event = False
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
    origin = input("Please enter the expected host IP address: ")
    app.logger.info("Target Host set: %s", origin)
    thread = Thread(target=arduino, args=(origin,))
    thread.daemon = True
    thread.start()
    app.logger.info("Arduino Thread started!")
    app.run(host="0.0.0.0", port=port)
