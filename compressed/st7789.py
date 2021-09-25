_B='Unsupported display. 320x240, 240x240 and 135x240 are supported.'
_A=None
import time
from micropython import const
import ustruct as struct
ST7789_NOP=const(0)
ST7789_SWRESET=const(1)
ST7789_RDDID=const(4)
ST7789_RDDST=const(9)
ST7789_SLPIN=const(16)
ST7789_SLPOUT=const(17)
ST7789_PTLON=const(18)
ST7789_NORON=const(19)
ST7789_INVOFF=const(32)
ST7789_INVON=const(33)
ST7789_DISPOFF=const(40)
ST7789_DISPON=const(41)
ST7789_CASET=const(42)
ST7789_RASET=const(43)
ST7789_RAMWR=const(44)
ST7789_RAMRD=const(46)
ST7789_PTLAR=const(48)
ST7789_VSCRDEF=const(51)
ST7789_COLMOD=const(58)
ST7789_MADCTL=const(54)
ST7789_VSCSAD=const(55)
ST7789_MADCTL_MY=const(128)
ST7789_MADCTL_MX=const(64)
ST7789_MADCTL_MV=const(32)
ST7789_MADCTL_ML=const(16)
ST7789_MADCTL_BGR=const(8)
ST7789_MADCTL_MH=const(4)
ST7789_MADCTL_RGB=const(0)
ST7789_RDID1=const(218)
ST7789_RDID2=const(219)
ST7789_RDID3=const(220)
ST7789_RDID4=const(221)
COLOR_MODE_65K=const(80)
COLOR_MODE_262K=const(96)
COLOR_MODE_12BIT=const(3)
COLOR_MODE_16BIT=const(5)
COLOR_MODE_18BIT=const(6)
COLOR_MODE_16M=const(7)
_ENCODE_PIXEL='>H'
_ENCODE_POS='>HH'
_DECODE_PIXEL='>BBB'
_BUFFER_SIZE=const(256)
_BIT7=const(128)
_BIT6=const(64)
_BIT5=const(32)
_BIT4=const(16)
_BIT3=const(8)
_BIT2=const(4)
_BIT1=const(2)
_BIT0=const(1)
WIDTH_320=[(320,240,0,0),(240,320,0,0),(320,240,0,0),(240,320,0,0)]
WIDTH_240=[(240,240,0,0),(240,240,0,0),(240,240,0,80),(240,240,80,0)]
WIDTH_135=[(135,240,52,40),(240,135,40,53),(135,240,53,40),(240,135,40,52)]
ROTATIONS=[0,96,192,160]
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
def _encode_pos(x,y):return struct.pack(_ENCODE_POS,x,y)
def _encode_pixel(color):return struct.pack(_ENCODE_PIXEL,color)
class ST7789:
	def __init__(A,spi,width,height,reset=_A,dc=_A,cs=_A,backlight=_A,rotation=0):
		D=height;C=width;B=backlight
		if D!=240 or C not in[320,240,135]:raise ValueError(_B)
		if dc is _A:raise ValueError('dc pin is required.')
		A._display_width=A.width=C;A._display_height=A.height=D;A.xstart=0;A.ystart=0;A.spi=spi;A.reset=reset;A.dc=dc;A.cs=cs;A.backlight=B;A._rotation=rotation%4;A.hard_reset();A.soft_reset();A.sleep_mode(False);A._set_color_mode(COLOR_MODE_65K|COLOR_MODE_16BIT);time.sleep_ms(5);A.rotation(A._rotation);A.inversion_mode(True);time.sleep_ms(5);A._write(ST7789_NORON);time.sleep_ms(5)
		if B is not _A:B.value(1)
		A.fill(0);A._write(ST7789_DISPON);time.sleep_ms(50)
	def _write(A,command=_A,data=_A):
		B=command
		if A.cs:A.cs.off()
		if B is not _A:A.dc.off();A.spi.write(bytes([B]))
		if data is not _A:
			A.dc.on();A.spi.write(data)
			if A.cs:A.cs.on()
	def hard_reset(A):
		if A.cs:A.cs.off()
		if A.reset:A.reset.on()
		time.sleep_ms(5)
		if A.reset:A.reset.off()
		time.sleep_ms(5)
		if A.reset:A.reset.on()
		time.sleep_ms(15)
		if A.cs:A.cs.on()
	def soft_reset(A):A._write(ST7789_SWRESET);time.sleep_ms(15)
	def sleep_mode(A,value):
		if value:A._write(ST7789_SLPIN)
		else:A._write(ST7789_SLPOUT)
	def inversion_mode(A,value):
		if value:A._write(ST7789_INVON)
		else:A._write(ST7789_INVOFF)
	def _set_color_mode(A,mode):A._write(ST7789_COLMOD,bytes([mode&119]))
	def rotation(A,rotation):
		B=rotation;B%=4;A._rotation=B;D=ROTATIONS[B]
		if A._display_width==320:C=WIDTH_320
		elif A._display_width==240:C=WIDTH_240
		elif A._display_width==135:C=WIDTH_135
		else:raise ValueError(_B)
		A.width,A.height,A.xstart,A.ystart=C[B];A._write(ST7789_MADCTL,bytes([D]))
	def _set_columns(A,start,end):
		B=start
		if B<=end<=A.width:A._write(ST7789_CASET,_encode_pos(B+A.xstart,end+A.xstart))
	def _set_rows(A,start,end):
		B=start
		if B<=end<=A.height:A._write(ST7789_RASET,_encode_pos(B+A.ystart,end+A.ystart))
	def _set_window(A,x0,y0,x1,y1):A._set_columns(x0,x1);A._set_rows(y0,y1);A._write(ST7789_RAMWR)
	def vline(A,x,y,length,color):A.fill_rect(x,y,1,length,color)
	def hline(A,x,y,length,color):A.fill_rect(x,y,length,1,color)
	def pixel(A,x,y,color):A._set_window(x,y,x,y);A._write(_A,_encode_pixel(color))
	def blit_buffer(A,buffer,x,y,width,height):A._set_window(x,y,x+width-1,y+height-1);A._write(_A,buffer)
	def rect(A,x,y,w,h,color):B=color;A.hline(x,y,w,B);A.vline(x,y,h,B);A.vline(x+w-1,y,h,B);A.hline(x,y+h-1,w,B)
	def fill_rect(A,x,y,width,height,color):
		C=height;B=width;A._set_window(x,y,x+B-1,y+C-1);D,E=divmod(B*C,_BUFFER_SIZE);F=_encode_pixel(color);A.dc.on()
		if D:
			G=F*_BUFFER_SIZE
			for H in range(D):A._write(_A,G)
		if E:A._write(_A,F*E)
	def fill(A,color):A.fill_rect(0,0,A.width,A.height,color)
	def line(F,x0,y0,x1,y1,color):
		G=color;D=y1;C=x1;B=y0;A=x0;H=abs(D-B)>abs(C-A)
		if H:A,B=B,A;C,D=D,C
		if A>C:A,C=C,A;B,D=D,B
		I=C-A;K=abs(D-B);E=I//2
		if B<D:J=1
		else:J=-1
		while A<=C:
			if H:F.pixel(B,A,G)
			else:F.pixel(A,B,G)
			E-=K
			if E<0:B+=J;E+=I
			A+=1
	def vscrdef(A,tfa,vsa,bfa):B='>HHH';struct.pack(B,tfa,vsa,bfa);A._write(ST7789_VSCRDEF,struct.pack(B,tfa,vsa,bfa))
	def vscsad(A,vssa):A._write(ST7789_VSCSAD,struct.pack('>H',vssa))
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
	def bitmap(B,bitmap,x,y,index=0):
		F=index;A=bitmap;G=A.HEIGHT*A.WIDTH;H=G*2;D=bytearray(H);E=A.BPP*G*F if F>0 else 0
		for I in range(0,H,2):
			C=0
			for M in range(A.BPP):C<<=1;C|=A.BITMAP[E//8]&1<<7-E%8>0;E+=1
			L=A.PALETTE[C];D[I]=L&65280>>8;D[I+1]=C&255
		J=x+A.WIDTH-1;K=y+A.HEIGHT-1
		if B.width>J and B.height>K:B._set_window(x,y,J,K);B._write(_A,D)
	@micropython.native
	def write(self,font,string,x,y,fg=WHITE,bg=BLACK):
		D=self;A=font;L=A.HEIGHT*A.MAX_WIDTH*2;C=bytearray(L);M=(fg&65280)>>8;N=fg&255;O=(bg&65280)>>8;P=bg&255
		for Q in string:
			try:
				H=A.MAP.index(Q);F=H*A.OFFSET_WIDTH;B=A.OFFSETS[F]
				if A.OFFSET_WIDTH>1:B=(B<<8)+A.OFFSETS[F+1]
				if A.OFFSET_WIDTH>2:B=(B<<8)+A.OFFSETS[F+2]
				G=A.WIDTHS[H];I=G*A.HEIGHT*2
				for E in range(0,I,2):
					if A.BITMAPS[B//8]&1<<7-B%8>0:C[E]=M;C[E+1]=N
					else:C[E]=O;C[E+1]=P
					B+=1
				J=x+G-1;K=y+A.HEIGHT-1
				if D.width>J and D.height>K:D._set_window(x,y,J,K);D._write(_A,C[0:I])
				x+=G
			except ValueError:pass