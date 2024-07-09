# import socket
# msgFromClient="KLOK from client"
# bytesToSend=msgFromClient.encode('utf-8')
# serverAddress = ('192.168.1.194', 2222)
# bufferSize=1024
# UDPClient=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# UDPClient.sendto(bytesToSend, serverAddress)
# data,address=UDPClient.recvfrom(bufferSize)
# data=data.decode('utf-8')
# print("Data from Server", data)
# print('Server IP Address: ', address[0])
# print("Server Port: ", address[1])
text1 = 'balls'
text2 ='tetas   '
print(f'ClientID: {text1}\nMessage: {text2}')