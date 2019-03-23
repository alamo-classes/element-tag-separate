"""
Used to capture photos of the LEGO Elements with corresponding labels to train the network
Training will only use the primary Raspberry Pi (#0 in the configuration file)
"""
import io
import os
from urllib import request
from PIL import Image


class CaptureLabeledImages:
    def __init__(self, arg_flags, config_args):
        self.rasp1_ip = config_args["Raspberry_IP"]["0"]
        self.train_data = "{}/train/".format(config_args["Artifacts"]["artifact_dir"])
        self.label = arg_flags.label
        os.makedirs(self.train_data, exist_ok=True)

    def get_snapshot(self):
        """
        Retrieve a snapshot from the Raspberry Pi camera. Then save the file and label.
        """
        # Get the next create the next iteration of the training data
        exit_command = None
        snaps_taken = 0
        capture_number = 0
        # While the user has not input the quit key
        while exit_command not in ['q, Q']:
            if exit_command in ['c', 'C']:
                self.label = input("Please enter the new label: ")
                capture_number = 0
            file = io.BytesIO(request.urlopen("{}/snapshot".format(self.rasp1_ip)).read())
            img = Image.open(file)
            exit_command = input("To take another snapshot press Enter.\n To change label enter \"c\".\n"
                                 "To quit enter \"q\": ")
            snaps_taken += 1
            # Check if there is a file with the current name, if so iterate...
            while os.path.exists("{}/{}_{}".format(self.train_data, self.label, capture_number)):
                capture_number += 1

            # Write the image file as a JPEG
            img.save("{}/{}_{}".format(self.train_data, self.label, capture_number))
            # Write the new column to the CSV
            # TODO: Put the CSV writer here. Need to figure out how the labels are taken first

        print("Successfully processed {} images for {} label".format(snaps_taken, self.label))
