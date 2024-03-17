import socket

UDP_IP = "127.0.0.1"  # Replace with your Unity IP address
UDP_PORT = 5000       # Replace with the Unity port number

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("Created Server")
while True:
    # Send data to Unity
	try:
		data = "Hello from Python!"
		sock.sendto(bytes(data, 'utf-8').encode(), (UDP_IP, UDP_PORT))
	except Exception as e :
		print(e)
