from machine import Pin,SoftSPI
import random, font,utime,gc,st7789
def time_acc_function(f,*D,**E):
	A=0;B=0.0
	def C(*C,**D):nonlocal A,B;E=utime.ticks_us();F=f(*C,**D);G=utime.ticks_diff(utime.ticks_us(),E);A+=1;B+=G;print('Function: {} Call count = {} Total time = {:6.3f}ms'.format(f.__name__,A,B/1000));return F
	return C
print('ready')
@time_acc_function
def main():A=SoftSPI(baudrate=800000000,polarity=1,sck=machine.Pin(18),mosi=machine.Pin(19),miso=Pin(13));B= st7789.ST7789(A, 135, 240, reset=Pin(23, Pin.OUT), cs=Pin(5, Pin.OUT), dc=Pin(16, Pin.OUT), backlight=Pin(4, Pin.OUT), rotation=0);return B
def run():
	A=main();print('GO');gc.collect()
	while True:
		for B in range(4):
			A.rotation(B);A.fill(st7789.BLACK);C= A.width - font.WIDTH * 6;D= A.height - font.HEIGHT
			for E in range(500):A.text(font,'Hello!', random.randint(0,C), random.randint(0,D),
									   st7789.color565(random.getrandbits(8), random.getrandbits(8), random.getrandbits(8)),
									   st7789.color565(random.getrandbits(8), random.getrandbits(8), random.getrandbits(8)))
run()