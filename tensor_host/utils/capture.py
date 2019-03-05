""" Used to capture photos of the LEGO Elements with corresponding labels to train the network """
import io
import os
from urllib import request
from PIL import Image


class CaptureLabeledImages:
    def __init__(self, ras1_ip, label):
        self.rasp1_ip = ras1_ip
        self.train_data = "{}/train/".format(os.getcwd())
        self.label = label
        self.iteration = 1
        os.makedirs(self.train_data, exist_ok=True)

    def get_snapshot(self):
        file = io.BytesIO(request.urlopen("{}/snapshot".format(self.rasp1_ip)).read())
        img = Image.open(file)

        # Get the next iteration number for the file name
        while os.path.exists("{}/{}_{}".format(self.train_data, self.label, self.iteration)):
            self.iteration += 1

        img.save('{}/{}_{}.jpg'.format(self.train_data, self.label, self.iteration))
