import serial
ard = serial.Serial("/dev/ttyACM0", 9600, timeout=5)
user_input = ""
while user_input is not "Z":
    user_input = input("Enter the next character: ")
    for cmd in list(user_input):
        ard.write(bytes(cmd, 'UTF-8'))
    print(ard.readline())
