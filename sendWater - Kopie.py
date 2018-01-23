import pifacecommon, pifacedigitalio
import os, string, time
import threading
import io
import socket
import ssl
import AWSIoTPythonSDK
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from os.path import expanduser
from datetime import datetime
import json

## Pyhton program to run on a raspberry PI with attache PiFaceDigitalIO board 
## The reed contact of water meter is contacted to PiFace board on input 0
## MEASURE: A closing of the contact will trigger the following action
## 1) LED-2 to toggle and
## 2) a timestamp being appended to the file ~/consumption.txt or created
## 3) an MQTT message being published to AWS IoT Service
##
##
## In case of suspicious water consumption an external relay is connected which controls a valve to shutdown the main water supply.
## The main water supply relay will be closed by a reaction on an incoming mqtt message.
## Message topic "anomaly-shutdown" will cause the following reaction:
## 1) LED-3 to go on.
## 2) External relay to close via OUTPUT PIN 7 to be on high
## Environment: Raspberry PI2 with PiFaceDigitalIO Board
## 1) External relay is being connected to
## Control: OUTPUT PIN 7
## Connection to 5V and GND
##
## 2) Reed contact water clock
## First wire to INPUT PIN 0
## Second wire to GND
##
## 3) AWS IoT connection requires the following files present
## RootCA file in                              ~/AWS/certs/aws-iot-rootCA.crt
## IoT Certificate in        ~/AWS/cert/cert.pem
## Private key in                              ~/AWS/cert/privkey.pem
##
## In addition to use AWS IoT the following variables need to be defined
## IOTendpoint = a1pw2oomauq0bh.iot.eu-central-1.amazonaws.com
###
## From PiFace documentation:
## INPUTS
## The eight input pins detect a connection to ground (provided as the ninth pin).
## The four switches are connected inparallel to the first four input pins. The inputs are pulled up to 5V. This can be turned off so that the inputs float.
## OUTPUTS
## The eight output pins are located at the top of the board (near the LEDs).
## The outputs are open collectors, they can bethought of as switches connecting to ground.
## This offers greater flexibility so that PiFace Digital can control devices that operate using different voltages. The ninth pin provides 5V for connecting circuits to.
## LEDS
## The LEDs are connected in parallel to each of the outputs. This means that when you set output pin 4 high, LED 4 illuminates.
##RELAYS
## The two Relays are connected in parallel to output pins 0 and 1 respectively. When you set output pin 0 high, LED 0 illuminates and Relay 0 activates.
#
# PIFace Digital IO LED / OUTPUT config 
# LED 0 - Reserved for integrated Relais 0
# LED 1 - Reserved for integrated Relais 1
# LED 2 - Toggled (on/off) with every litre water 
# LED 3 - not used
# LED 4 - Not used 
# LED 5 - Switched on if MQTT Message ANOMALY received 
# LED 6 - Switched on if MQTT Message ANOMALY received with 1s delay after LED 5
# LED 7 - Switched on if MQTT Message ANOMALY received with 3s delay. Connected to relais it will close to main water. 
#
#TODO SCETION
# A - Start as deamon


## AWS IOT Parameters ##
awshost = "[DELETED-for-github.com].iot.eu-central-1.amazonaws.com" # need to take endpoint from environment variable to not expose this to public 
awsport = 8883
clientId = "raspi2"
thingName = "raspi2"
rootCAPath = "/home/pi/AWS/cert/aws-iot-rootCA.crt"  #RootCA file
certificatePath = "/home/pi/AWS/cert/cert.pem"       # Device IoT Certificate
privateKeyPath = "/home/pi/AWS/cert/privkey.pem"     # Private key
## end parameter section for IoT config ##                      
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)

		
#Log consumption to a file
def appendLineToFile(lines):
	pass
	#home = expanduser("~")
	#logfile = str(home) + "/consumption.txt"	
	#log("Logfile:" + logfile)
	#mode = 'a+' if os.path.exists(logfile) else 'w+'
	#myfile = open(logfile, mode)
	#myFile.writelines(lines)
	#myFile.close()
	

## Code partially taken from https://github.com/mariocannistra/python-paho-mqtt-for-aws-iot/blob/master/awsiotsub.py
## and https://github.com/aws/aws-iot-device-sdk-python/blob/master/samples/basicPubSub/basicPubSubAsync.py                         
def on_connect(client, userdata, flags, rc):
	log ("Connection returned result: " + str(rc) )
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	client.subscribe("#" , 1 )
	

# incoming_message callback
def incoming_message(message):
	log("Received incoming_message ")
	log(message)
	print(message.payload)
	print("from topic: ")
	print(message.topic)
	print("--------------\n\n")
	if (message.topic == "TEST"):
		log ("received TEST message via MQTT")
	if (message.topic == "ANOMALY"):
		log ("received ANOMALY message via MQTT")		
		pfd.output_pins[5].value = 1
		sleep(1)
		pfd.output_pins[6].value = 1
		sleep(1)
		pfd.output_pins[6].value = 1	
			   
			   
# Suback callback
def customSubackCallback(mid, data):
	log("Received SUBACK packet id: ")
	log(mid)
	log("Granted QoS: ")
	log(data)
	log("++++++++++++++\n\n")
			   
# Publish acknowledge callback - not sure if needed  at all for this 
def customPubackCallback(mid):
	log("Received PUBACK packet id: ")
	log(mid)
	log("++++++++++++++\n\n")

def log(message):          
	## Default log behavior is a print
	print "Log ", datetime.now().strftime('%Y-%m-%d %H:%M:%S'), message

# Publish a message	to AWS IoT Service
def sendTick(message):	
	myAWSIoTMQTTClient.publishAsync("Water", message, 1, ackCallback=customPubackCallback)
				   
# Publish 10 MQTT messages for testing purposes 			   
def testConnection():
	# Publish to the same topic in a loop 10 times with a second delay in between
	loopCount = 0
	while loopCount < 11:
		myAWSIoTMQTTClient.publishAsync(topic, "New TestMessage " + str(loopCount), 1, ackCallback=customPubackCallback)
		loopCount += 1
		time.sleep(1)
                 
## Callback from pifacedigitalio libs                                
def waterTick(event):
    #Called when a liter is through
	event.chip.leds[2].toggle() #Toggle LED for each litre
	timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')	
	## for logging to file ##
	#appendLineToFile(timestamp)      
	
	log("1 Liter at " + timestamp + " written to logfile.")  
	log ("Sending MQTT Message...")  
	MQTT_MSG=json.dumps({"waterTick": timestamp, "source": "raspi2", "atHome":  "TRUE"})
	log (MQTT_MSG)
	## Send to mqtt code goes here                                 
	sendTick(MQTT_MSG)


def main():
	pfd = pifacedigitalio.PiFaceDigital()
	log("Piface init done")   
	#Prepare AWS IoT Service			
	#myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
	## DISABLE extra metric collection by AWS
	myAWSIoTMQTTClient.disableMetricsCollection()
	myAWSIoTMQTTClient.disableMetricsCollection()	
	log("awshost" + awshost) 
	log("rootCAPath:" + rootCAPath)
	log("privateKeyPath: " + privateKeyPath)
	log(" certificatePath:" + certificatePath)
	myAWSIoTMQTTClient.configureEndpoint(awshost, awsport)	
	myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
	# AWSIoTMQTTClient connection configuration
	myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
	myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
	myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
	myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
	myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
	#Define callback for incoming messages
	myAWSIoTMQTTClient.onMessage = incoming_message                         
	# Connect and subscribe to AWS IoT
	myAWSIoTMQTTClient.connect()                                           
	myAWSIoTMQTTClient.subscribeAsync("WATER_CONTROL", 1, ackCallback=customSubackCallback)
	
	               
	listener = pifacedigitalio.InputEventListener()
	## Listen to contact s in input 0
	listener.register(0, pifacedigitalio.IODIR_FALLING_EDGE, waterTick )
	log("Listener registered")
	try:	
		listener.activate()
		log("Listener activated")   
	except:
		exit()
		
	
if __name__ == '__main__':
    main()