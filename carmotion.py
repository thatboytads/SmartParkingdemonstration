from gpiozero import MotionSensor
from gpiozero import LED
import time
from datetime import datetime

class CarSensor:
	def __init__(self):        
		self.cnt1= False 
		self.cnt2= False
		self.parked=0

	def motion_detect(self,pir1, pir2,buzz):
		try:
			current_time=[]
			#sensed_time=""
			while True:
				cnt=pir1.motion_detected 
				if cnt==True and self.parked==0: #if motion is detected and the car is not parked
					print("Front wheel has been sensed by 1st")
					print("Waiting for back wheel to be sensed by 1nd")
					time.sleep(2)
					if pir1.wait_for_motion(2):#waits 2 seconds to see if back wheel sesned by 1st sensor
						print("back wheel sensed by 1st ")
						print("Waiting for the front tip to be sensed by 2nd")
						if pir2.wait_for_motion(2):#wait 2 seconds to see if second motion sensor detects front of car
							#once parked
                            print("tip sensed by 2nd")
							print("Car in")
							buzz.on()
							time.sleep(3)
							buzz.off()
							self.parked=1
							message= "car parked"
							return message #return that the car is parked to the API class
							continue
				cnt2=pir2.motion_detected 
				if cnt2==True and self.parked==1: #if motion is detected again and the car is parked
					print("Tip sensed moving back by 2nd")
					print("Waiting for back wheel to be sensed 1st")
					if pir1.wait_for_motion(2):#waits 2 seconds to see if the back motion sensor detects the back of the car moving
						print("back wheel been sensed by 1st")
						print("waiting for front wheel to be sensed by 1st")
						time.sleep(2)
						if pir1.wait_for_motion(2):#wait 2 seconds to see if back sensor sensors front of car
							print("front wheel sensed by 1st")
							print("car out")
							buzz.on()
							time.sleep(3)
							buzz.off()
							self.parked=0
							message= "car not parked"
							return message #return that the car is not parked anymore to the API class
							continue
		except KeyboardInterrupt:
			pass


