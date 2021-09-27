# --- #


import socket
from machine import Timer
import gc

import ftptiny
import html as ht


print(f"MAIN INIT\n")


def do_connect_sta():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('NETGEAR90', 'curlyearth685')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())


def do_connect_ap():
    import network
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid="TTGO-TEST")
    if not ap.isconnected():
        print('Creating network...')
        while not ap.isconnected():
            pass
    print('network config:', ap.ifconfig())


def tick():
    print("5 Seconds")


def write(dat):
    with open('data') as f:
        f.write(dat)
        return


""" -------------------------------------------------- """

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", 80))
    s.listen(5)
except OSError:
    import machine
    machine.reset()


def web_serv():
    main_page = (ht.http + ht.title_01 + ht.style + ht.index)

    while True:
        try:
            conn, addr = s.accept()
            req = conn.recv(4096)
            if len(req) == 0:
                conn.close()
                return
            else:
                # Do something wth the received data...
                print("Received: {}".format(str(req)))  # uncomment this line to view the HTTP request
                gc.collect()

            if "GET / " in str(req):
                # this is a get response for the page
                # Sends back some data
                conn.send(main_page)
                conn.close()

            if "GET /?led=on " in str(req):
                print(f"LED on")
                conn.send(main_page)
                conn.close()

            if "GET /?led=off " in str(req):
                print(f"LED on")
                conn.send(main_page)
                conn.close()

            if "GET /?reset " in str(req):
                from machine import deepsleep
                conn.close()
                deepsleep(500)

            if "GET /?ftp " in str(req):
                conn.send(main_page)
                ftp = ftptiny.FtpTiny()
                ftp.start()
                conn.close()

        except OSError:
            s.close()
            print('Connection closed')


tim = Timer(1)
tim.init(period=5000, mode=Timer.PERIODIC, callback=lambda t: tick())

do_connect_sta()

print(f"SERVER START\n")
web_serv()

