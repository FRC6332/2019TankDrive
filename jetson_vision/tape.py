import zmq
context = zmq.Context()
angle_socket = context.socket(zmq.PUB)
angle_socket.connect('tcp://localhost:5556')

while True:
	#VISION CODE
	angle_socket.send(angle)