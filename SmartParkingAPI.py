# USAGE


# import the necessary packages
import cameraSensor
import carmotion
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import time
import cv2
from livereload import Server
from gpiozero import MotionSensor
from gpiozero import LED
import time
import threading
import argparse
pir1=MotionSensor(17)# set the first motion sensor to pin 17
pir2=MotionSensor(27)# set the second motion sensor to pin 27
buzz=LED(4)#set the buzzer to zero




# initialize a flask object
app = Flask(__name__)



time.sleep(2.0);
lock = threading.Lock()
vs = VideoStream(src=0).start()
motion= carmotion.CarSensor()
cam= cameraSensor.CarCamera(lock,vs)
message= "car not parked"


#this is the first route which returns both motion detection and offers camera surveilance
@app.route('/ParkingAPI',methods=['GET'])
def full_parking():
	message= motion.motion_detect(pir1,pir2,buzz)
	if (message=="car parked"):
		return render_template("sensorTrue.html")
	else:
		return render_template("sensorFalse.html")

#here is the second route which offers only motion detection to users
@app.route('/motionAPI',methods=['GET'])
def motion_parking():
	message= motion.motion_detect(pir1,pir2,buzz)
	if (message=="car parked"):
		return render_template("motionTrue.html")
	else:
		return render_template("motionFalse.html")
#here is the third option which just offers camera surveilance to users
@app.route('/cameraAPI',methods=['GET'])
def camera_parking():
    return render_template("camera.html")
#this route generates the video stream as required
@app.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(cam.generate(),mimetype = "multipart/x-mixed-replace; boundary=frame")



	

if __name__ == '__main__':

	t = threading.Thread(target=cam.setup_frames,)#initiates the threading for the camera
	t.daemon = True
	t.start()#starts the thread
	ap = argparse.ArgumentParser()
    #gives users the ability to add arguments  for differnt ports and for a differnt IP addresss on their respective raspberry pi
	ap.add_argument("-i", "--ip", type=str, required=True,
		help="ip address of the device")
    
	ap.add_argument("-o", "--port", type=int, required=True,
		help="ephemeral port number of the server (1024 to 65535)")
	args = vars(ap.parse_args())
	app.run(host=args["ip"], port=args["port"], debug=True,
		threaded=True, use_reloader=False)


# release the video stream pointer
vs.stop()
