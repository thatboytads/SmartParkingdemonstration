from imutils.video import VideoStream
import imutils
import time
import cv2

class CarCamera:
	def __init__(self,lock,vs):
		self.output_frame = None
		self.lock = lock
		self.vs = vs
		time.sleep(2.0)

	def setup_frames(self):
		while True:
			# read the next frame from the video stream, resize it,
			# convert the frame to grayscale, and blur it
			frame = self.vs.read()
			frame = imutils.resize(frame, width=400)
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			gray = cv2.GaussianBlur(gray, (7, 7), 0)
			with self.lock:
				self.output_frame = frame.copy()
	def generate(self):
		while(True):
			with self.lock:
			# check if the output frame is available, otherwise skip
			# the iteration of the loop
				if self.output_frame is None:
					continue

			# encode the frame in JPEG format
				(flag, encodedImage) = cv2.imencode(".jpg", self.output_frame)

			# ensure the frame was successfully encoded
				if not flag:
					continue

			# yield the output frame in the byte format
			yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
				bytearray(encodedImage) + b'\r\n')
	
