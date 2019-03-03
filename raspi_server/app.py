#!flask/bin/python
from flask import Flask, jsonify, send_file
import logging
from logging import Formatter, FileHandler
import os
from picamera import PiCamera

app = Flask(__name__)
camera = PiCamera()
camera.resolution = (1920, 1080)
camera.start_preview()


@app.route('/')
def index():
    return "Connection Active: Ready to receive commands!"


@app.route('/snapshot')
def snapshot():
    """
    Return a snapshot as a JPEG mimetype
    :return: MIME object
    """
    camera.capture('snapshot.jpg')
    return send_file('snapshot.jpg', mimetype='image/jpg')


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
