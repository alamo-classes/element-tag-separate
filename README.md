# element-tag-separate
LEGO Element Image Based Sorting Smart Assistant

# Synopsis
The element sorter is an automated system to identify and respectively sort
LEGO elements using an image convolutional neural network (CNN). The system is distributed onto three different 
OS/Hardward platforms: Ubuntu, RaspberryPi (Raspbian Stretch), Arduino. 

The Ubuntu platform hosts the TensorFlow recognition system as well as a web server through Django. 

The Raspberry Pi runs three different processes as services:
1. Flask web server - Receives commands and requests from the Django-based web client. Passes commands to Arduino controller process.  
2. Arduino controller - Receives commands from flask and passes serial commands to the Raspberry Pi.
3. Video stream - Accesses the camera resource and streams video in MJPEG format.

The Arduino platform controls all servos, sensors, and LED lighting.

# System Layout
![Schematic of Mechanical Layout](images/schematic_1.jpg)
---
# Getting Started
This repo is divided into two sets of code. The "tensorhost" code will be placed on the Ubuntu platform. The 
"raspberry_controller" will be placed on the Raspberry Pi platform. For more explanation of setup, please refer to the
documentation in each respective folder

---
# Workflow
## Tag
When fed from the bulk feeder, the part will tagged with a confidence interval by the Tensorflow image recognition
neural network. If the element is recognized with an appropriate confidence interval the LEGO element 
will be sorted based on its part number and color, cross referenced by category.
## Separate
The automated servos will sort the LEGO element into a category bin based on the current sorting profile. By using
successive sorting profiles, it will become possible to sort elements into more discreet groups.
## Three Pass System
1. Category - Sort the bulk lego into successively more discreet categories.
2. Part Number - Once divided into a sufficient category, the part may then be sorted by part number.
3. Color - Once divided into the respective part number, the part may be further sorted by color.
---
# GUI Interface (TODO)
* Link youtube video
* Learning for adding parts
* Mode for Separate (Category, Part Number, Color)
* Advanced Mode for Set Detection
