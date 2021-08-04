#CODE FOR SMART GARAGE DOOR OPENER

import bluetooth
import RPi.GPIO as GPIO
import time
import signal
import sys
import thingspeak


GPIO.setmode(GPIO.BCM)


#pin numbers for ultrasonic sensor
trig=23
echo=24

#pin number for IR sensor
beamPin=4

#door pins
openPin=21
closePin=20

GPIO.setmode(GPIO.BCM)

GPIO.setup(trig,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)
GPIO.setup(beamPin,GPIO.IN)
GPIO.setup(openPin,GPIO.OUT)
GPIO.setup(closePin,GPIO.OUT)


#thingspeak information
channel_id = 799513 # channel ID from your Thingspeak channel
write_key = 'CW7I7V6QQBTMQDE3' # obtain from Thingspeak
#read_key = 'VAF8ZKF59Q60AVIF'
url = 'https://api.thinkspeak.com/update' # default URL to update Thingspeak
ts = thingspeak.Channel(channel_id, write_key, url)
#ts_read = thingspeak.Channel(channel_id,read_key,url)

carHeight=26

#Signal handler to catch Ctrl+c and exit gracefully 
def signal_handler(sig, frame):
        print("\nExiting Program")
        GPIO.cleanup
        sys.exit(0)
signal.signal(signal.SIGINT,signal_handler)

#setup for bluetooth connection
def btsetup():

    connected = False 
    print("Running btsetup")
    bluetooth_addr = "00:14:03:05:5A:61" # The address from the HC-05 sensor
    bluetooth_port = 1 # Channel 1 for RFCOMM

    #loop that waits to establish connection with arduino
    while not connected:
        
        try:          
             
            bluetoothSocket = bluetooth.BluetoothSocket (bluetooth.RFCOMM)
            bluetoothSocket.connect((bluetooth_addr,bluetooth_port))
            psw=bluetoothSocket.recv(1024)
            if psw:
                connected=True
                
            else:
                connected=False
               
        except:
            connected = False
            time.sleep(3)


    return

#This gets the distance from the ultrasonic sensor
def getDistance():

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(openPin,GPIO.OUT)
    GPIO.setup(closePin,GPIO.OUT)
    GPIO.setup(trig,GPIO.OUT)
    GPIO.setup(echo,GPIO.IN)
    GPIO.output(trig,False)
    time.sleep(2)

    GPIO.output(trig,True)
    time.sleep(0.00001)
    GPIO.output(trig,False)

    while GPIO.input(echo)==0:
        pulse_start=time.time()

    while GPIO.input(echo)==1:
        pulse_end=time.time()

    pulse_duration=pulse_end-pulse_start

    distance=pulse_duration*17150
    distance=round(distance,2)

    #print("Distance:",distance,"cm")
    GPIO.cleanup()
    return distance


def openDoor():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(20,GPIO.OUT)
    GPIO.setup(21,GPIO.OUT)

    GPIO.output(20,False)
    GPIO.output(21,True)
    return
        
def closeDoor():
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(20,GPIO.OUT)
    GPIO.setup(21,GPIO.OUT)

    print("Door Closing")

    i=5
    while i>0:
        time.sleep(1)
        if beam()==0:
            print("Door Blocked")
            i=5
        else:
            print(i)
            i=i-1
    GPIO.output(21,False)
    GPIO.output(20,True)
    return
        
def beam():
    #print("in beam") 
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(20,GPIO.OUT)
    GPIO.setup(21,GPIO.OUT)
    GPIO.setup(beamPin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    return GPIO.input(beamPin)
    

GPIO.output(20,True)
while True:
    

    btsetup()

    
    #print("after bt") 
    
    #car is approaching garage from outside
    if getDistance()>carHeight:
        
        openDoor()
        #print("after open") 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(openPin,GPIO.OUT)
        GPIO.setup(closePin,GPIO.OUT)
        while getDistance()>carHeight:
            #print(getDistance())
            time.sleep(0.01) #wait till conditions are met
        thingspeak_field1={"field1":"0","status":"Parked"}
        #print("before thingspeak")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(openPin,GPIO.OUT)
        GPIO.setup(closePin,GPIO.OUT)
        ts.update(thingspeak_field1)
        closeDoor()
        time.sleep(5)
    #car is parked in garage when it connects    
    else:
        openDoor()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(openPin,GPIO.OUT)
        GPIO.setup(closePin,GPIO.OUT)
        while getDistance()<=carHeight:
            pass #wait till car is out of driveway

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(openPin,GPIO.OUT)
        GPIO.setup(closePin,GPIO.OUT)
        thingspeak_field1={"field1":"1","status":"Left"}
        ts.update(thingspeak_field1)
              
        closeDoor()
        time.sleep(5)