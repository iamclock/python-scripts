#! /usr/bin/python3

import socket






server_adress = ('localhost', 0xAAAA)
server_name = "Server#1: "
print(server_adress)

socket_descriptor = socket.socket()
socket_descriptor.bind(server_adress)
socket_descriptor.listen(1)
new_sock_desc, addr = socket_descriptor.accept()
new_sock_desc.send(b"You Are connected\nType something: ")

while True:
	string = new_sock_desc.recv(1024)
	string = server_name + string.decode("utf-8") + '\n' + "More: "
	new_sock_desc.send(string.encode())

new_sock_desc.close()
