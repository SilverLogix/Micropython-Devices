def space_free():from os import statvfs as B;A=B('/flash');C=A[0];D=A[3];E=C*D;F=1024*1024;G=E/F;print('Free space:'+str(G))
def m_freq():import machine as B;A=str(B.freq());print('Mhz: '+A);return A
def raw_temp():import esp32;B=str(esp32.raw_temperature());A='CPU Temp: '+B+'F';print(A);C=A;return C
def showVoltage():from machine import ADC,Pin;B=ADC(Pin(32));C=int(1100);D=B.read();E=float(D)/4095.0*2.0*3.3*(C/1000.0);A='Voltage: {0:0.2f}v'.format(E);print(A);F=A;return F
def getmac():import network as A,ubinascii as B;C=B.hexlify(A.WLAN(1).config('mac'),':').decode();print(str(C))
def pprint():import gc;print('');print('-------------------');getmac();space_free();m_freq();raw_temp();showVoltage();print('--------------------');print('');gc.collect()