# - #


# import ftptiny
import network
import socket
import _thread

spinner = ["|", "/", "-", "\\", "|", "/", "-", "\\"]
for i in spinner:
    print(spinner)


def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('NETGEAR90', 'curlyearth685')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())


do_connect()


# Thread for handling a client
def client_thread(clientsockett, n):
    # Receive maxium of 12 bytes from the client
    r = clientsockett.recv(4096)

    # If recv() returns with 0 the other end closed the connection
    if len(r) == 0:
        clientsockett.close()
        return
    else:
        # Do something wth the received data...
        print("Received: {}".format(str(r)))  # uncomment this line to view the HTTP request

    http = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection:close \r\n\r\n"  # HTTP response

    if "GET / " in str(r):
        # this is a get response for the page
        # Sends back some data
        clientsockett.send(http + "<html><body><h1> You are connection " + str(
            n) + "</h1><br> Your browser will send multiple requests <br> <a href='/hello'> hello!</a><br><a href='/color'>change led color!</a></body></html>")
    elif "GET /hello " in str(r):

        clientsockett.send(http + "<html><body><h1> Hello to you too! </h1><br> <a href='/'> go back </a></body></html>")
    elif "GET /color" in str(r):
        clientsockett.send(http + "<html><body><h1> You are connection " + str(
            n) + "</h1><br> Your browser will send multiple requests <br> <a href='/hello'> hello!</a><br><a href='/color'>change led color!</a></body></html>")

    # Close the socket and terminate the thread

    clientsockett.close()


# Set up server socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(("192.168.4.1", 80))

# Accept maximum of 5 connections at the same time
serversocket.listen(5)

# Unique data to send back
c = 1
while True:
    # Accept the connection of the clients
    (clientsocket, address) = serversocket.accept()
    # Start a new thread to handle the client
    _thread.start_new_thread(client_thread, (clientsocket, c))
    c = c + 1
    serversocket.close()
