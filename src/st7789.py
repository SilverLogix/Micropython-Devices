_B='Unsupported display. 320x240, 240x240 and 135x240 are supported.'
_A=None
import time
from micropython import const
import ustruct as struct
NOP=const(0)
SWRESET=const(1)
RDDID=const(4)
RDDST=const(9)
SLPIN=const(16)
SLPOUT=const(17)
PTLON=const(18)
NORON=const(19)
INVOFF=const(32)
INVON=const(33)
DISPOFF=const(40)
DISPON=const(41)
CASET=const(42)
RASET=const(43)
RAMWR=const(44)
RAMRD=const(46)
PTLAR=const(48)
VSCRDEF=const(51)
COLMOD=const(58)
MADCTL=const(54)
VSCSAD=const(55)
MY=const(128)
MX=const(64)
MV=const(32)
ML=const(16)
BGR=const(8)
MH=const(4)
RGB=const(0)
RDID1=const(218)
RDID2=const(219)
RDID3=const(220)
RDID4=const(221)
C_65K=const(80)
C_262K=const(96)
C_12BIT=const(3)
C_16BIT=const(5)
C_18BIT=const(6)
C_16M=const(7)
_ENCODE_PIXEL='>H'
_ENCODE_POS='>HH'
_DECODE_PIXEL='>BBB'
_BUFF=const(256)
_BIT7=const(128)
_BIT6=const(64)
_BIT5=const(32)
_BIT4=const(16)
_BIT3=const(8)
_BIT2=const(4)
_BIT1=const(2)
_BIT0=const(1)
W320=[(320,240,0,0),(240,320,0,0),(320,240,0,0),(240,320,0,0)]
W240=[(240,240,0,0),(240,240,0,0),(240,240,0,80),(240,240,80,0)]
W135=[(135,240,52,40),(240,135,40,53),(135,240,53,40),(240,135,40,52)]
ROTS=[0,96,192,160]
@micropython.native
def color565(aR,aG,aB):return(aR&248)<<8|(aG&252)<<3|aB>>3
BLACK=0
RED=color565(255,0,0)
MAROON=color565(128,0,0)
GREEN=color565(0,255,0)
FOREST=color565(0,128,128)
BLUE=color565(0,0,255)
NAVY=color565(0,0,128)
CYAN=color565(0,255,255)
YELLOW=color565(255,255,0)
PURPLE=color565(255,0,255)
WHITE=color565(255,255,255)
GRAY=color565(128,128,128)
@micropython.viper
def _encode_pos(x,y):return struct.pack(_ENCODE_POS,x,y)
@micropython.viper
def _encode_pixel(color):return struct.pack(_ENCODE_PIXEL,color)
class ST7789:
	def __init__(A,spi,width,height,reset=_A,dc=_A,cs=_A,backlight=_A,rotation=0):
		D=height;C=width;B=backlight
		if D!=240 or C not in[320,240,135]:raise ValueError(_B)
		if dc is _A:raise ValueError('dc pin is required.')
		A._display_width=A.width=C;A._display_height=A.height=D;A.xstart=0;A.ystart=0;A.spi=spi;A.reset=reset;A.dc=dc;A.cs=cs;A.backlight=B;A._rotation=rotation%4;A.hard_reset();A.soft_reset();A.sleep_mode(False);A._set_color_mode(C_65K|C_16BIT);A.rotation(A._rotation);A.inversion_mode(True);A._write(NORON);
		if B is not _A:B.value(1)
		A.fill(0);A._write(DISPON);time.sleep_ms(1)
	@micropython.native
	def _write(self,command=_A,data=_A):
		B=command;A=self
		if A.cs:A.cs.off()
		if B is not _A:A.dc(0);A.spi.write(bytes([B]))
		if data is not _A:
			A.dc.on();A.spi.write(data)
			if A.cs:A.cs(1)
	def hard_reset(A):
		if A.cs:A.cs(0)
		if A.reset:A.reset(1)
		time.sleep_ms(5)
		if A.reset:A.reset(0)
		time.sleep_ms(5)
		if A.reset:A.reset(1)
		time.sleep_ms(5)
		if A.cs:A.cs(1)
	def soft_reset(A):A._write(SWRESET);time.sleep_ms(5)
	@micropython.native
	def sleep_mode(self,value):
		if value:self._write(SLPIN)
		else:self._write(SLPOUT)
	def inversion_mode(A,value):
		if value:A._write(INVON)
		else:A._write(INVOFF)
	@micropython.native
	def _set_color_mode(self,mode):self._write(COLMOD,bytes([mode&119]))
	@micropython.native
	def rotation(self,rotation):
		B=rotation;A=self;B%=4;A._rotation=B;D=ROTS[B]
		if A._display_width==320:C=W320
		elif A._display_width==240:C=W240
		elif A._display_width==135:C=W135
		else:raise ValueError(_B)
		A.width,A.height,A.xstart,A.ystart=C[B];A._write(MADCTL,bytes([D]))
	def _set_columns(A,start,end):
		B=start
		if B<=end<=A.width:A._write(CASET,_encode_pos(B+A.xstart,end+A.xstart))
	def _set_rows(A,start,end):
		B=start
		if B<=end<=A.height:A._write(RASET,_encode_pos(B+A.ystart,end+A.ystart))
	def _set_window(A,x0,y0,x1,y1):A._set_columns(x0,x1);A._set_rows(y0,y1);A._write(RAMWR)
	@micropython.native
	def on(self,aTF=True):self._write(DISPON if aTF else DISPON)
	@micropython.native
	def vline(self,x,y,length,color):self.fill_rect(x,y,1,length,color)
	@micropython.native
	def hline(self,x,y,length,color):self.fill_rect(x,y,length,1,color)
	@micropython.native
	def pixel(self,x,y,color):self._set_window(x,y,x,y);self._write(_A,_encode_pixel(color))
	@micropython.native
	def blit_buffer(self,buffer,x,y,width,height):self._set_window(x,y,x+width-1,y+height-1);self._write(_A,buffer)
	@micropython.native
	def rect(self,x,y,w,h,color):B=color;A=self;A.hline(x,y,w,B);A.vline(x,y,h,B);A.vline(x+w-1,y,h,B);A.hline(x,y+h-1,w,B)
	@micropython.native
	def fill_rect(self,x,y,width,height,color):
		C=height;B=width;A=self;A._set_window(x,y,x+B-1,y+C-1);D,E=divmod(B*C,_BUFF);F=_encode_pixel(color);A.dc.on()
		if D:
			G=F*_BUFF
			for H in range(D):A._write(_A,G)
		if E:A._write(_A,F*E)
	@micropython.native
	def triangle(self,x0,y0,x1,y1,x2,y2,color):B=color;A=self;A.line(x0,y0,x1,y1,B);A.line(x1,y1,x2,y2,B);A.line(x2,y2,x0,y0,B)
	@micropython.native
	def fill(self,color):A=self;A.fill_rect(0,0,A.width,A.height,color)
	@micropython.native
	def line(self,x0,y0,x1,y1,color):
		F=color;D=y1;C=x1;B=y0;A=x0;G=abs(D-B)>abs(C-A)
		if G:A,B=B,A;C,D=D,C
		if A>C:A,C=C,A;B,D=D,B
		H=C-A;J=abs(D-B);E=H//2
		if B<D:I=1
		else:I=-1
		while A<=C:
			if G:self.pixel(B,A,F)
			else:self.pixel(A,B,F)
			E-=J
			if E<0:B+=I;E+=H
			A+=1
	@micropython.native
	def vscrdef(self,tfa,vsa,bfa):A='>HHH';struct.pack(A,tfa,vsa,bfa);self._write(VSCRDEF,struct.pack(A,tfa,vsa,bfa))
	@micropython.native
	def vscsad(self,vssa):self._write(VSCSAD,struct.pack('>H',vssa))
	def _text16(E,font,text,x0,y0,color=WHITE,background=BLACK):
		C=background;B=color;A=font
		for K in text:
			F=ord(K)
			if A.FIRST<=F<A.LAST and x0+A.WIDTH<=E.width and y0+A.HEIGHT<=E.height:
				if A.HEIGHT==16:G=2;H=32;I=16
				else:G=4;H=64;I=16
				for J in range(G):D=(F-A.FIRST)*H+I*J;L=struct.pack('>128H',B if A.FONT[D]&_BIT7 else C,B if A.FONT[D]&_BIT6 else C,B if A.FONT[D]&_BIT5 else C,B if A.FONT[D]&_BIT4 else C,B if A.FONT[D]&_BIT3 else C,B if A.FONT[D]&_BIT2 else C,B if A.FONT[D]&_BIT1 else C,B if A.FONT[D]&_BIT0 else C,B if A.FONT[D+1]&_BIT7 else C,B if A.FONT[D+1]&_BIT6 else C,B if A.FONT[D+1]&_BIT5 else C,B if A.FONT[D+1]&_BIT4 else C,B if A.FONT[D+1]&_BIT3 else C,B if A.FONT[D+1]&_BIT2 else C,B if A.FONT[D+1]&_BIT1 else C,B if A.FONT[D+1]&_BIT0 else C,B if A.FONT[D+2]&_BIT7 else C,B if A.FONT[D+2]&_BIT6 else C,B if A.FONT[D+2]&_BIT5 else C,B if A.FONT[D+2]&_BIT4 else C,B if A.FONT[D+2]&_BIT3 else C,B if A.FONT[D+2]&_BIT2 else C,B if A.FONT[D+2]&_BIT1 else C,B if A.FONT[D+2]&_BIT0 else C,B if A.FONT[D+3]&_BIT7 else C,B if A.FONT[D+3]&_BIT6 else C,B if A.FONT[D+3]&_BIT5 else C,B if A.FONT[D+3]&_BIT4 else C,B if A.FONT[D+3]&_BIT3 else C,B if A.FONT[D+3]&_BIT2 else C,B if A.FONT[D+3]&_BIT1 else C,B if A.FONT[D+3]&_BIT0 else C,B if A.FONT[D+4]&_BIT7 else C,B if A.FONT[D+4]&_BIT6 else C,B if A.FONT[D+4]&_BIT5 else C,B if A.FONT[D+4]&_BIT4 else C,B if A.FONT[D+4]&_BIT3 else C,B if A.FONT[D+4]&_BIT2 else C,B if A.FONT[D+4]&_BIT1 else C,B if A.FONT[D+4]&_BIT0 else C,B if A.FONT[D+5]&_BIT7 else C,B if A.FONT[D+5]&_BIT6 else C,B if A.FONT[D+5]&_BIT5 else C,B if A.FONT[D+5]&_BIT4 else C,B if A.FONT[D+5]&_BIT3 else C,B if A.FONT[D+5]&_BIT2 else C,B if A.FONT[D+5]&_BIT1 else C,B if A.FONT[D+5]&_BIT0 else C,B if A.FONT[D+6]&_BIT7 else C,B if A.FONT[D+6]&_BIT6 else C,B if A.FONT[D+6]&_BIT5 else C,B if A.FONT[D+6]&_BIT4 else C,B if A.FONT[D+6]&_BIT3 else C,B if A.FONT[D+6]&_BIT2 else C,B if A.FONT[D+6]&_BIT1 else C,B if A.FONT[D+6]&_BIT0 else C,B if A.FONT[D+7]&_BIT7 else C,B if A.FONT[D+7]&_BIT6 else C,B if A.FONT[D+7]&_BIT5 else C,B if A.FONT[D+7]&_BIT4 else C,B if A.FONT[D+7]&_BIT3 else C,B if A.FONT[D+7]&_BIT2 else C,B if A.FONT[D+7]&_BIT1 else C,B if A.FONT[D+7]&_BIT0 else C,B if A.FONT[D+8]&_BIT7 else C,B if A.FONT[D+8]&_BIT6 else C,B if A.FONT[D+8]&_BIT5 else C,B if A.FONT[D+8]&_BIT4 else C,B if A.FONT[D+8]&_BIT3 else C,B if A.FONT[D+8]&_BIT2 else C,B if A.FONT[D+8]&_BIT1 else C,B if A.FONT[D+8]&_BIT0 else C,B if A.FONT[D+9]&_BIT7 else C,B if A.FONT[D+9]&_BIT6 else C,B if A.FONT[D+9]&_BIT5 else C,B if A.FONT[D+9]&_BIT4 else C,B if A.FONT[D+9]&_BIT3 else C,B if A.FONT[D+9]&_BIT2 else C,B if A.FONT[D+9]&_BIT1 else C,B if A.FONT[D+9]&_BIT0 else C,B if A.FONT[D+10]&_BIT7 else C,B if A.FONT[D+10]&_BIT6 else C,B if A.FONT[D+10]&_BIT5 else C,B if A.FONT[D+10]&_BIT4 else C,B if A.FONT[D+10]&_BIT3 else C,B if A.FONT[D+10]&_BIT2 else C,B if A.FONT[D+10]&_BIT1 else C,B if A.FONT[D+10]&_BIT0 else C,B if A.FONT[D+11]&_BIT7 else C,B if A.FONT[D+11]&_BIT6 else C,B if A.FONT[D+11]&_BIT5 else C,B if A.FONT[D+11]&_BIT4 else C,B if A.FONT[D+11]&_BIT3 else C,B if A.FONT[D+11]&_BIT2 else C,B if A.FONT[D+11]&_BIT1 else C,B if A.FONT[D+11]&_BIT0 else C,B if A.FONT[D+12]&_BIT7 else C,B if A.FONT[D+12]&_BIT6 else C,B if A.FONT[D+12]&_BIT5 else C,B if A.FONT[D+12]&_BIT4 else C,B if A.FONT[D+12]&_BIT3 else C,B if A.FONT[D+12]&_BIT2 else C,B if A.FONT[D+12]&_BIT1 else C,B if A.FONT[D+12]&_BIT0 else C,B if A.FONT[D+13]&_BIT7 else C,B if A.FONT[D+13]&_BIT6 else C,B if A.FONT[D+13]&_BIT5 else C,B if A.FONT[D+13]&_BIT4 else C,B if A.FONT[D+13]&_BIT3 else C,B if A.FONT[D+13]&_BIT2 else C,B if A.FONT[D+13]&_BIT1 else C,B if A.FONT[D+13]&_BIT0 else C,B if A.FONT[D+14]&_BIT7 else C,B if A.FONT[D+14]&_BIT6 else C,B if A.FONT[D+14]&_BIT5 else C,B if A.FONT[D+14]&_BIT4 else C,B if A.FONT[D+14]&_BIT3 else C,B if A.FONT[D+14]&_BIT2 else C,B if A.FONT[D+14]&_BIT1 else C,B if A.FONT[D+14]&_BIT0 else C,B if A.FONT[D+15]&_BIT7 else C,B if A.FONT[D+15]&_BIT6 else C,B if A.FONT[D+15]&_BIT5 else C,B if A.FONT[D+15]&_BIT4 else C,B if A.FONT[D+15]&_BIT3 else C,B if A.FONT[D+15]&_BIT2 else C,B if A.FONT[D+15]&_BIT1 else C,B if A.FONT[D+15]&_BIT0 else C);E.blit_buffer(L,x0,y0+8*J,16,8)
			x0+=A.WIDTH
	@micropython.native
	def text(self,font,text,x0,y0,color=WHITE,background=BLACK):
		if font.WIDTH==16:self._text16(font,text,x0,y0,color,background)
	@micropython.native
	def bitmap(self,bitmap,x,y,index=0):
		F=index;B=self;A=bitmap;G=A.HEIGHT*A.WIDTH;H=G*2;D=bytearray(H);E=A.BPP*G*F if F>0 else 0
		for I in range(0,H,2):
			C=0
			for M in range(A.BPP):C<<=1;C|=A.BITMAP[E//8]&1<<7-E%8>0;E+=1
			L=A.PALETTE[C];D[I]=L&65280>>8;D[I+1]=C&255
		J=x+A.WIDTH-1;K=y+A.HEIGHT-1
		if B.width>J and B.height>K:B._set_window(x,y,J,K);B._write(_A,D)