# This file is executed on every boot (including wake-boot from deepsleep)


# import esp
# esp.osdebug(None)

import gc

import machine
import network
#import webrepl


# DO NOT GO BELOW 80Mhz!!!  Will break wifi and complicate serial!

# machine.freq(240000000) # set the CPU frequency to 240 MHz
#machine.freq(160000000)  # set the CPU frequency to 160 MHz
machine.freq(80000000)  # set the CPU frequency to 80 MHz

ap = network.WLAN(network.AP_IF)


def hotspot(ssid, maxc, on):
    ap.config(essid=ssid)
    ap.config(max_clients=maxc)
    ap.active(on)


#webrepl.start(password="password")
hotspot("ESP-AP", 2, True)

# network.WLAN(0).active(False)
# network.WLAN(1).active(False)

gc.collect()
