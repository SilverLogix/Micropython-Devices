import gc
T=True
F=gc.collect
import machine
x=machine.freq
import network
r=network.AP_IF
n=network.WLAN
import webrepl
D=webrepl.start
x(80000000)
ap=n(r)
def B(ssid,maxc,on):
 ap.config(essid=ssid)
 ap.config(max_clients=maxc)
 ap.active(on)
D(password="password")
B("ESP-AP",2,T)
F()
