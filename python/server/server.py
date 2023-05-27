import socket

server = socket.socket()
server.bind(("0.0.0.0", 5000))

server.listen(5)
while True:

    s, a = server.accept()

    b = s.recv(100)

    print(b)

    s.send(b)
