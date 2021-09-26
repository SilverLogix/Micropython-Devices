# - #


import network
import socket
import _thread
import gc
import utime

# Customs
# import ftptiny
import html as H


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


def memget():
    mf = gc.mem_free()
    print(f"{mf} free")


do_connect()


# Set up server socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(("192.168.1.25", 80))

# Accept maximum of 5 connections at the same time
serversocket.listen(5)


# Thread for handling a client
def client_thread(clientsocket, n):
    # Receive maxium of 12 bytes from the client
    r = clientsocket.recv(4096)

    # If recv() returns with 0 the other end closed the connection
    if len(r) == 0:
        clientsocket.close()
        return
    else:
        # Do something wth the received data...
        print("Received: {}".format(str(r)))  # uncomment this line to view the HTTP request

    if "GET / " in str(r):
        # this is a get response for the page
        # Sends back some data
        clientsocket.send(H.http + H.index)
    elif "GET /hello " in str(r):

        clientsocket.send(H.http + f"<html><body><h1> Hello to you too! </h1><br> <a href='/'> go back </a></body></html>")
    elif "GET /color" in str(r):
        clientsocket.send(H.http + f"<html><body><h1> You are connection " + str(
            n) + f"</h1><br> Your browser will send multiple requests <br> <a href='/hello'> hello!</a><br><a href='/color'>change led color!</a></body></html>")

    # Close the socket and terminate the thread

    clientsocket.close()
    gc.collect()
    _thread.exit()


# Unique data to send back
c = 1
while True:
    # Accept the connection of the clients
    (clientsocket, address) = serversocket.accept()
    # Start a new thread to handle the client
    _thread.start_new_thread(client_thread, (clientsocket, c))
    c = c + 1
    # serversocket.close()
