# IoT-GarageOpener
ECE 442 Final Project

## Description
  This system relies on two microcomputers, the Raspberry Pi 3B and the Arduino UNO.  The Arduino UNO is inside of the car and runs off of the cars battery.  The Raspberry Pi is inside of the garage connected to two different sensors and the garage door opener.  If the car is inside the garage and the power is turned to devices in the car then the Arduino UNO will connect to the Raspberry Pi and send it a password, if the password is correct then the garage door will open automatically.  Once the Arduino UNO inside the car is out of range of the Raspberry Pie and nothing is blocking the door then the door will close.  When the car is approaching the garage from outside and the Arduino UNO is in range of the Raspberry Pi the garage door will open.  Once the car is parked and off and nothing is in the way of the garage door then it will close.  The goal is to have a smart garage door that opens automatically for the user when they are leaving or entering in their car.
    Another functionality of this system is that it will record when a car leaves or enters the garage to the cloud.  This adds a home monitoring aspect to the system which is helpful to the user if they suspect someone is using their vehicle unauthorized or at an unauthorized time.  This is also a proof of concept proving that the data from the garage can be collected or actions can be taken from the cloud remotely from the home network. 
    
## Hardware
The hardware used for the demo was: Raspberry Pi 3B, Arduino UNO, HC-06 Bluetooth Transmitter, HC-SR04 Ultrasonic Sensors, and Adafruit beam-break sensors.  The following is a description of these devices and sensors:

   * **Raspberry Pi 3B** – The Raspberry Pi is a microcomputer that was developed for students, hobbyists, and computer enthusiasts to learn programming skills and for use in DIY projects. There are various models of Raspberry Pi out today ranging in specs and size.  The Raspberry Pi 3B specs are:
        * Broadcom BCM2837 1.2GHz 64-bit quad-core, ARMv8 Cortex-A53 CPU
        * Broadcom VideoCore IV GPU
        * 1GB LPDDR2 (900MHz)
        * 10/100 Ethernet
        * 2.4GHz 802.11n wireless
        * Bluetooth 4.1 (Classic, Bluetooth LE)
        * microSD storage
        * 40-pin GPIO header
        * HDMI
        * 3.5mm audio jack
        * 4xUSB 2.0
        * Ethernet
        * Camera Serial Interface
        * Display Serial Interface
   * **Arduino UNO** – The Arduino UNO is another microcomputer but is less powerful than the Raspberry Pi.  As with the Raspberry Pi, there are many different models of Arduino.  The specifications for the Arduino UNO are:
        * ATmega328p microcontroller
        * 5V operating voltage
        * Recommended input voltage: 7-12V
        * Input voltage limits: 6-20V
        * 14 digital I/O pins
        * 6 Analog input pins
        * DC current per I/O pin: 20mA
        * DC current for 3.3V pin: 50mA
        * Weight: 25g
   * **HC-06 Bluetooth Transmitter** – The HC-06 is a classic Bluetooth transmitter.  This is a Bluetooth class 2 device.  This is a simple slave device meaning that it can only connect to other devices that are initiating a connection, it can not discover other devices on its own.  The specifications of this device are:
        * Bluetooth class 2
        * 3.1V~4V
        * 2.4GHz wireless transceiver
        * FHSS (frequency hopping spread spectrum)
   * **HC-SR04 Ultrasonic Sensor** – The HC-SR04 is an ultrasonic sensor that uses ultrasonic waves to determine the distance of an object in front of it.  To do this it emits an 8 cycle burst of ultrasound at 40kHz then raises on echo.  Using the time t starting from the emission and the return echo the distance is calculated as: 
	The specifications of this devices is:
        * 5V working voltage
        * Range: 2cm-4m
        * Trigger 10µs TTL pulse
   * **Adafruit beam-break sensor** – The Adafruit beam-break sensor is a combination of an IR sensor and an IR emitter.  The IR emitter shoots a beam of IR light at the reciever, if the beam is broken then the senor sends a signal notifying that something is blocking the signal.  The specifications of this device are:
        * Range: up to 50 cm
        * Faster and more narrow than a PIR sensor
        * Less exspensive than ultrasonic sensor
        * When beam is broken: LOW. Otherwise: HIGH
   * **Sensor Interfacing** – The HC-SR04 and Adafruit beam-break sensors are interfaced to the Raspberry Pi.  The HC-06 is interfaced to the Arduino UNO.  The HC-06 has only 4 pins: transmit, receive, power, ground.  The transmit and receive GPIO ports on the Arduino are the same as the ones used by the USB so it is important to setup different GPIO pins to be used as the transmit/recieve pins for the HC-06.  Below is an example of the wiring:

![HC-06 Arduino](https://user-images.githubusercontent.com/46805337/128111975-54916cdd-93bf-4ff9-955a-c6d74cb06837.png)

![HC-SR04 pi](https://user-images.githubusercontent.com/46805337/128112040-757a007e-1ddf-40e2-8b5a-9d4a7183494d.png)

The HC-SR04 requires 5V for operation and outputs 5V.  This causes a bit of an issue because the digital GPIO pins of the Raspberry Pi are not rated for 5V input and this could possibly damage the unit.  Because of this I created a simple voltage divider circuit to make sure that the voltage going into the Raspberry Pi was around 3.3V.  Below is a schematic of the circuit used:
![voltage divider schematic](https://user-images.githubusercontent.com/46805337/128112127-88e3d51f-6335-4e0f-b99b-d988575477c6.png)


    
