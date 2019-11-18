# element-tag-separate
LEGO Element Image Based Sorting Smart Assistant

# Introduction
The element sorter is an automated system to identify and respectively sort
LEGO elements using an image convolutional neural network (CNN). The system is distributed onto four different 
OS/Hardward platforms: Ubuntu, RaspberryPi controller (Raspbian Stretch), RaspberryPi camera, Arduino. 

The Ubuntu platform hosts the TensorFlow recognition system as well as a web server through Django. 

The Raspberry Pi controller runs three different processes as services:
1. Flask web server - Receives commands and requests from the Django-based web client. Passes commands to Arduino controller process.  
2. Arduino controller - Receives commands from flask and passes serial commands to the Raspberry Pi.
3. Video stream - Accesses the camera resource and streams video in MJPEG format.

The Raspberry Pi camera runs only the Video stream as it does not need to communicate actively with any other system.

The Arduino platform controls all servos, sensors, and LED lighting.

# System Layout
![Schematic of Mechanical Layout](images/schematic_1.jpg)
---
# Getting Started
This repo is divided into two sets of code. The "tensorhost" code will be placed on the Ubuntu platform. The 
"raspberry_controller" will be placed on the Raspberry Pi platform. For more explanation of setup, please refer to the
documentation in each respective folder

---
# System Process Workflow
## Capture
After a block model is created in the database, the automatic system can take photos of the model from the mounted cameras.
Since this process is automated, the user will only need to fill the hopper with the same part and allow the system to feed through the parts.
The entire capture process is controlled through the web ui.
## Training
Once a enough captures of blocks are taken (200+), it is possible to train a new neural network. The process is automated
through the web ui. The Django backend view will create the appropriate file/folder structure and then spawn a new thread
responsible for training the network.
## Sorting
When fed from the bulk feeder, the part will tagged with a confidence interval by the respective trained CNN. 
If the element is recognized with an appropriate confidence interval it will be assigned a position based on the profile mapping.
The position will correlate to a physical bin where the block will be sorted.
---
# User Interface
For an in-depth explanation, please see the following youtube video explaining how the web ui interact with the system.

[![Lego Element Sorter](images/video_screenshot.png)](https://youtu.be/cp-qN7oeIuc "Lego Element Sorter")

## User Interface Workflow
### Settings
The settings page is responsible for some of the global settings needed by the UI. It is required before the capture 
process begins and can be updated any time by clicking the "Settings" tab in the menu bar.
### Blocks
The blocks application is used to enter a block into the database. The part number (found from collector catalogs) as well
as physical characteristics are entered into the database. The blocks table will display the entered parts and the number of
training photos that each block respectively has. 
### Capture
TODO: Add an image
The capture application uses the blocks entered in the Blocks application. To start a capture, select the block that is
training data should be produced. Load the machine's hopper with multiple copies of the part. Click the run button to start
the capture process. To end the capture click the red button.
### Training
Once enough training data is captured for multiple blocks, the UI will allow you to train a new neural network. Select 
eligible blocks that you would like to use in the network and submit the form. A background thread is started to train the new
network. Once the network is finished, the table will display the finished status.
### Profiles
Profiles are used to map the labels found in a network to physical bin locations. There are six assignable bins as well 
as a seventh bin used for sorting un-sortable pieces. 
### Sorting
TODO: Add an image
Select a defined profile and click the green run button. Parts will be sorted into their respective bins.
### Catalog
TODO
### Admin
There is a "hidden" administrative panel which allows developers to directly interact with the database. This can be useful when
debugging certain applications; however, caution is advised when using this page. Incorrectly interacting with the database
can cause system instability.
