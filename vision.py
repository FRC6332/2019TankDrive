import zmq
import base64
import numpy as np
from cscore import CameraServer

def main():
	#set up camera server
	cs=CameraServer.getInstance()
	cs.enableLogging()
	outputStream = cs.putVideo("Sandstream", 320, 240)
	#set up zmq and init an empty image frame
	context = zmq.Context()
	footage_socket = context.socket(zmq.SUB)
	footage_socket.bind('tcp://*:5555')
	footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))
	img = np.zeros(shape=(240, 320, 3), dtype=np.uint8)
	while True:
		frame = footage_socket.recv_string()
		img = base64.b64decode(frame)
		npimg = np.fromstring(img, dtype=np.uint8) #converts 1-dimensional array into 2d numpy array
		#source = cv2.imdecode(npimg, 1)
		outputStream.putFrame(npimg)