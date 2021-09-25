_B='Connection successful'
_A=True
@micropython.native
def STA(ssid,passw):
	import network as B;A=B.WLAN(B.STA_IF);A.active(_A);A.connect(ssid,passw)
	while not A.isconnected():0
	print(_B);print(A.ifconfig());return A
@micropython.native
def SSSTA(ssid,passw,static,routerip):
	B=routerip;import network as C;A=C.WLAN(C.STA_IF);A.ifconfig((static,'255.255.255.0',B,B));A.active(_A);A.connect(ssid,passw)
	while not A.isconnected():0
	print(_B);print(A.ifconfig());return A
@micropython.native
def AP(ssid,maxc,pswd):import network as B;A=B.WLAN(B.AP_IF);A.config(essid=ssid);A.config(max_clients=maxc);A.config(password=pswd);A.active(_A);print(_B);print(A.ifconfig());return A
@micropython.native
def Wkill(cmd):import network as A;A.WLAN(0).active(cmd);A.WLAN(1).active(cmd)