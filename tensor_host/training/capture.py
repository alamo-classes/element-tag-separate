"""
Used to capture photos of the LEGO Elements with corresponding labels to train the network
Training will only use the primary Raspberry Pi (#0 in the configuration file)
"""
import io
import os
import sys
import uuid
from urllib import request
from PIL import Image
import pandas as pd

from settings.models import ElementSettings


class CaptureLabeledImages:
    def __init__(self, label):
        settings_file = ElementSettings.objects.first()
        self.rasp1_ip = settings_file.rasp1_ip
        self.train_data = os.path.join(os.getcwd(), '../artifacts/train/')
        self.df_path = os.path.join(os.getcwd(), '../artifacts/labels.csv')
        self.label = label
        os.makedirs(self.train_data, exist_ok=True)

    def get_snapshot(self):
        """
        Retrieve a snapshot from the Raspberry Pi camera. Then save the file and label.
        """
        # Get the next create the next iteration of the training_old data
        exit_command = None
        snaps_taken = 0
        capture_number = 0
        # While the user has not input the quit key
        while True:
            if exit_command in ['c', 'C']:
                self.label = input("Please enter the new label: ")
                capture_number = 0
            file = io.BytesIO(request.urlopen("http://{}:5000/snapshot".format(self.rasp1_ip)).read())
            img = Image.open(file)
            exit_command = input("To take another snapshot press Enter.\n To change label enter \"c\".\n"
                                 "To quit enter \"q\": ")
            if exit_command in ['q', 'Q']:
                print("Successfully logged {} images!".format(snaps_taken))
                exit(0)
            snaps_taken += 1
            # Check if there is a file with the current name, if so iterate...
            while os.path.exists("{}/{}_{}".format(self.train_data, self.label, capture_number)):
                capture_number += 1

            # Write the image file as a JPEG.
            unique_id = uuid.uuid4().hex
            img.save("{}/{}.jpg".format(self.train_data, unique_id))
            # Write the new column to the data frame
            df = pd.DataFrame({'id': [unique_id], 'part_num': [self.label]}, columns=['id', 'part_num'])
            # Append the dataframe to the csv file. If the file does not exist then write the headers as well.
            with open(self.df_path, 'a') as csv_file:
                df.to_csv(csv_file, header=(csv_file.tell() == 0), index=False)
