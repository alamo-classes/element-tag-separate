# Installing Arduino CLI and deploying code to the Arduino
## Compile and install GO, then compile the "arduino-cli" binary
```
wget https://storage.googleapis.com/golang/go1.11.8.linux-armv6l.tar.gz
sudo tar -C /usr/local -xzf go1.11.8.linux-armv6l.tar.gz 
export PATH=$PATH:/usr/local/go/bin
export GOPATH="$HOME/go/"
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
cd ~/.arduino15/
wget https://downloads.arduino.cc/packages/package_index.json
~/go/bin/arduino-cli board list
```

## Uploading sketch using CLI
Find the connected board
``` 
arduino-cli board list
```

Install the correct core library. The one used here is an AVR Mega
``` 
arduino-cli core install arduino:avr
```

Download any needed libraries
``` 
arduino-cli lib install "Servo"
arduino-cli lib install "Adafruit NeoPixel"
```

Compile the sketch and upload
``` 
arduino-cli compile --fqbn arduino:avr:mega $HOME/Arduino/test_servo
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:mega $HOME/Arduino/test_servo
```

# Setup of python services
## Download needed files from apt repository
## Setup python virtual environment
TODO: git clone <raspberry_pi_dir>
TODO: virtualenv -? /usr/bin/python3.6 venv
source venv/bin/activate
pip install -r requirements.txt
## Install services
sudo cp video_stream.service /etc/systemd/system/
sudo cp flask.service /etc/systemd/system/
sudo service video_stream enable
sudo service video_stream start
sudo service flask enable
sudo service flask start
