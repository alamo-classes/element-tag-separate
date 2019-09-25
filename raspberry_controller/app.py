#!flask/bin/python
import sys
from threading import Thread, Event
from time import sleep

import json
import requests
import serial
from flask import Flask, jsonify, send_file, Response
import logging
from logging import Formatter, FileHandler
import os
from picamera import PiCamera
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # TODO: Look into making this only work from host origin


class DetectionThread(Thread):
    def __init__(self, stop_event, sorting, group=None):
        super(DetectionThread, self).__init__(group, stop_event, sorting)
        self.camera = PiCamera()
        self.camera.resolution = (1920, 1080)
        self.stop_event = stop_event
        self.sorting = sorting
        self.arduino_serial = serial.Serial("/dev/ttyACM0", 9600, timeout=5)  # TODO: See if timeout should be lower
        self.url = "192.168.4.12:8000/profile/"

    def run(self):
        sleep(5)
        print("Running", file=sys.stderr)
        while not self.stop_event.is_set():
            print("Running right now", file=sys.stderr)
            print("Sorting Flag is: {}".format(self.sorting.is_set(), file=sys.stderr))
            sleep(5)
            # # Begin first stage of detection. Send command to start detection loop to arduino.
            # self.arduino_serial.write(bytes('m', 'UTF-8'))
            #
            # # Wait for the IR detection to trigger
            # detected=False
            # while not detected:
            #     log = self.arduino_serial.readline().decode()
            #     # TODO: Use function to send log via REST
            #     if "Detected" in log:
            #         break
            #
            # # Take a new snapshot
            # self.camera.capture('{}/snapshot.jpg'.format(os.getcwd()))
            #
            # # Send request for Tensor Flow server to begin processing. Wait for response.
            # if self.sorting.is_set:
            #     position = requests.get(url=self.url + "detection_sorting_alert")
            # else:
            #     position = requests.get(url=self.url + "detection_training_alert")
            # position = position.json()
            #
            # # Determine if this is training or sorting mode
            # if position['mode'] == 'training':
            #     # Send part through sorter in training position
            #     self.arduino_serial.write(bytes('', 'UTF-8'))
            #     # Sleep 2 seconds and then continue loop
            #     sleep(2)
            # else:
            #     # Move sorter and pass block to correct bin
            #     self.arduino_serial.write(bytes('', 'UTF-8'))
            #     # Sleep 2 seconds and then continue loop
            #     sleep(2)


# Create/set the stop event. Initialize the thread.
STOP_EVENT = Event()
SORTING = Event()
thread = DetectionThread(STOP_EVENT, SORTING)
thread.daemon = True
STOP_EVENT.set()


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
    return "No snapshot taken. Please wait for process to run.", 200


@app.route('/detection_training')
def detection_training():
    """ Start the training detection loop """
    STOP_EVENT.clear()
    return json.dumps({'success': True}), 200


@app.route('/detection_sorting')
def detection_sorting():
    """ Start the sorting detection loop """
    STOP_EVENT.clear()
    SORTING.set()
    return "Detection loop started for sorting. Beginning detection loop", 200


@app.route('/stop_detection')
def stop_detection():
    """ Stop the detection loop """
    STOP_EVENT.set()
    SORTING.clear()
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
    thread.start()
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
