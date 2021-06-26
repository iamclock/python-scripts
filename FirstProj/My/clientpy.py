#! /usr/bin/python3

import socket



server_adress = ('localhost', 0xAAAA)


print(server_adress)

socket_descriptor = socket.socket()
socket_descriptor.connect(server_adress)
string = socket_descriptor.recv(1024)

while True:
	string = input(string.decode("utf-8"));
	if string == "shutdown":
		break;
	socket_descriptor.send(string.encode())
	string = socket_descriptor.recv(1024)

socket_descriptor.close()