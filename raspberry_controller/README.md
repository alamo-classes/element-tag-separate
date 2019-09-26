## Installing Arduino CLI
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