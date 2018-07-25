#! /usr/bin/env python

import RPi.GPIO as GPIO
import sys
import select
from azure.servicebus import *
import os
import threading
import time

AZURE_SERVICEBUS_NAMESPACE='stv-svcbus'
AZURE_SERVICEBUS_SHARED_KEY_NAME='RootManageSharedAccessKey'
AZURE_SERVICEBUS_ACCESS_KEY_VALUE='SRvOQ7O5LXP+vvrc0pUImxwvrn+m/IdyODbzobnH3B0='
GPIO_BCM_PIN = 21 


def process_messages():    # Initialize the service bus
    service_bus = ServiceBusService(service_namespace=AZURE_SERVICEBUS_NAMESPACE, shared_access_key_name=AZURE_SERVICEBUS_SHARED_KEY_NAME, shared_access_key_value = AZURE_SERVICEBUS_ACCESS_KEY_VALUE)

    service_bus.get_topic("light-topic")
    service_bus.get_subscription("light-topic","light-subscription")
    while True:      
        msg = service_bus.receive_subscription_message('light-topic', 'light-subscription', peek_lock=False)
	if msg.body is not None:
	    print(msg.body)
            try:
	        if msg.custom_properties["led"] == 1:
		    print("turning on the LED")
		    GPIO.output(GPIO_BCM_PIN, 1)
                    continue

	        if msg.custom_properties["led"] == 0:
		    print("turning off the LED")
		    GPIO.output(GPIO_BCM_PIN, 0)
                    '''
                    continue
                
                if msg.custom_properties["led"] == 2:
                    print "Enjoy the show!"
                    ctr = 0
                    GPIO.output(GPIO_BCM_PIN, 0)
                    while(ctr != 15):
                        GPIO.output(GPIO_BCM_PIN, 1)
                        time.sleep(1)
                        GPIO.output(GPIO_BCM_PIN, 0)
                        time.sleep(1)
                        ctr += 1
                    print "The End!"
                    '''
                else:
                    print "Unrecognized instruction"
            except:
                pass
				

if __name__ == '__main__':
    # setup the GPIO for the LED
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_BCM_PIN,GPIO.OUT)
    # Initially turn off the LED
    GPIO.output(GPIO_BCM_PIN, 0)

    # start a thread listening for incoming messages
    t = threading.Thread(target=process_messages) #will create 'process_messages' next step
    t.daemon=True;
    t.start()

    # wait until the user enters something
    char = raw_input("Press enter to exit program")
    # release any GPIO resources
    GPIO.cleanup()


