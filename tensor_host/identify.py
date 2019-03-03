import io
import os
import sys
from urllib import request
from PIL import Image


class Training:
    def __init__(self, ras1_ip):
        self.rasp1_ip = ras1_ip

    def get_snapshot(self):
        file = io.BytesIO(request.urlopen("{}/snapshot".format(self.rasp1_ip)).read())
        img = Image.open(file)
        img.save('test.jpg')

    def train(self):
        pass


class Identify:
    def __init__(self):
        pass

    def identify_element(self):
        pass


if __name__ == "__main__":
    # Get arguments, if arguments not found then
    try:
        if sys.argv[1] not in ["training", "category_1", "category_2", "color_1"]:
            raise IndexError
    except IndexError:
        print("Please enter one of the following modes:\n"
              "\"training\" - Training Mode\n"
              "\"category_1\" - Perform Category 1 Sorting\n"
              "\"category_2\" - Perform Category 2 Sorting\n"
              )
        exit(0)
    # If not already created, generate an artifacts directory
    os.makedirs(path="{}/artifacts".format(os.chdir), exist_ok=True)
    # Set the Raspberry Pi IP
    # TODO: Put this in a configuration file
    rasp1_ip = "http://192.168.0.117:5000"
    # Run routine based on the cli argument
    if sys.argv[1] == "training":
        trainer = Training(rasp1_ip)
        trainer.get_snapshot()
