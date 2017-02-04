from __future__ import print_function
import RPi.GPIO as GPIO
import time
import sys
import logging
from hx711 import HX711
from ISStreamer.Streamer import Streamer

streamer = Streamer(bucket_name="feed cookie 3000", bucket_key="NLELHBGCPER6", access_key="4i49qQcSpJDzoaY09iMGGvfTBwg6Iyd0") 

def cleanAndExit():
    print ("Cleaning...")
    GPIO.cleanup()
    print ("Bye!")
    sys.exit()

def powerCycle():
	hx.power_down()
	hx.power_up()
	time.sleep(3)

GPIO.cleanup()

hx = HX711(24,23)
hx.set_reading_format("LSB", "MSB")
hx.set_reference_unit(360)

hx.reset()
hx.tare()

logging.basicConfig(filename='cookie.log', format='%(asctime)s %(message)s', level = logging.INFO)

while True:
	try:
		powerCycle()
		val = hx.get_weight(5)
		
		streamer.log("remaining food", val)
		logging.info('remaining food %s', val) 

		if val<7:
			streamer.log("remaining food", "commited feed")

                        logging.info('commited feed')

			GPIO.setup(17, GPIO.OUT)
			p= GPIO.PWM(17,50)
			p.start(7.5)

			p.ChangeDutyCycle(11.25)
			time.sleep(2)
			p.ChangeDutyCycle(3.45)
			time.sleep(2)
			p.stop()
			GPIO.cleanup(17)
			powerCycle()
			val = hx.get_weight(5)
			
			streamer.log("remaining food", val)
			
			logging.info('remaining food %s', val)	

			if val <=0:
				streamer.log("remaining food", "no food left")
				
				logging.warning('remaining food no food left') 

				GPIO.cleanup()
				sys.exit()
		hx.power_down()
		time.sleep(900)
	except (KeyboardInterrupt, SystemExit):
		cleanAndExit()
