_E='\r\n'
_D=False
_C=True
_B=None
_A='/'
import _thread,gc,os,socket,network
DATA_PORT=13333
class FtpTiny:
	def __init__(A):A.dorun=_C;A.isrunning=_D;A.cwd=os.getcwd();A.ftpsocket=_B;A.datasocket=_B;A.dataclient=_B
	def start_listen(A):B='0.0.0.0';A.ftpsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM);A.datasocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM);A.ftpsocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1);A.datasocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1);A.ftpsocket.bind(socket.getaddrinfo(B,21)[0][4]);A.datasocket.bind(socket.getaddrinfo(B,DATA_PORT)[0][4]);A.ftpsocket.listen(1);A.datasocket.listen(1);A.datasocket.settimeout(10);A.lastpayload=''
	def send_list_data(A,client):
		for B in os.listdir(A.cwd):C=os.stat(A.get_absolute_path(B));D='drwxr-xr-x'if C[0]&61440==16384 else'-rw-r--r--';E=C[6];F='{}    1 owner group {:>13} Jan 1  1980 {}'.format(D,E,B);A.sendcmdline(client,F)
	def send_file_data(C,path,client):
		with open(path)as B:
			A=B.read(128)
			while len(A)>0:
				client.sendall(A)
				if len(A)==128:A=B.read(128)
				else:A=[]
	def save_file_data(D,path,client):
		B=client;B.settimeout(0.5)
		with open(path,'w')as C:
			try:
				A=B.recv(128)
				while A and len(A)>0:
					C.write(A)
					if len(A)==128:A=B.recv(128)
					else:A=_B
			except Exception as E:pass
	def get_absolute_path(C,payload):
		B=payload;A=B
		if not B.startswith(_A):
			if len(C.cwd)>1:A=C.cwd+_A+B
			else:A=C.cwd+B
		if len(A)>1:return A.rstrip(_A)
		return A
	def stop(A):A.dorun=_D;A.thread=0
	def start(A):
		if not A.isrunning:A.dorun=_C;B=_thread.start_new_thread(runserver,(A,));A.thread=B
		else:print('An instance is already running.')
	def sendcmdline(A,cl,txt):cl.sendall(txt);cl.sendall(_E)
	def closeclient(A):
		if A.dataclient:A.dataclient.close();A.dataclient=_B
	def client(A,cl):return A.dataclient if A.dataclient else cl
	def _handle_command(A,cl,command,payload):
		Q='Failed to delete folder: ';P='550 Failed to delete file.';O='550 Failed to send file';N='226 Transfer complete.';M='502';L='SYST';F=payload;C=command;B=cl
		if C=='USER':A.sendcmdline(B,'230 Logged in.')
		elif C==L:A.sendcmdline(B,'215 ESP32 MicroPython')
		elif C==L:A.sendcmdline(B,M)
		elif C=='PWD':A.sendcmdline(B,'257 "{}"'.format(A.cwd))
		elif C=='CWD':
			D=A.get_absolute_path(F)
			try:os.chdir(D);A.sendcmdline(B,'250 Directory changed successfully')
			except:A.sendcmdline(B,'550 Failed to change directory')
			finally:A.cwd=os.getcwd()
		elif C=='EPSV':A.sendcmdline(B,M)
		elif C=='TYPE':A.sendcmdline(B,'200 Transfer mode set')
		elif C=='SIZE':
			D=A.get_absolute_path(F)
			try:H=os.stat(D)[6];A.sendcmdline(B,'213 {}'.format(H))
			except:A.sendcmdline(B,'550 Could not get file size')
		elif C=='QUIT':A.sendcmdline(B,'221 Bye.')
		elif C=='PASV':I=network.WLAN().ifconfig()[0];A.sendcmdline(B,'227 Entering Passive Mode ({},{},{}).'.format(I.replace('.',','),DATA_PORT>>8,DATA_PORT%256));A.dataclient,J=A.datasocket.accept();print('FTP Data connection from:',J)
		elif C=='LIST':
			try:A.send_list_data(A.client(B));A.closeclient();A.sendcmdline(B,'150 Here comes the directory listing.');A.sendcmdline(B,'226 Listed.')
			except:A.sendcmdline(B,'550 Failed to list directory')
			finally:A.closeclient()
		elif C=='RETR':
			try:A.send_file_data(A.get_absolute_path(F),A.client(B));A.closeclient();A.sendcmdline(B,'150 Opening data connection.');A.sendcmdline(B,N)
			except:A.sendcmdline(B,O)
			A.closeclient()
		elif C=='STOR':
			try:A.sendcmdline(B,'150 Ok to send data.');A.save_file_data(A.get_absolute_path(F),A.client(B));A.closeclient();print('Finished receiving file');A.sendcmdline(B,N)
			except Exception as E:print('Failed to receive file: '+str(E));A.sendcmdline(B,O)
			finally:print('Finally closing dataclient');A.closeclient()
		elif C=='DELE':
			try:D=A.get_absolute_path(F);os.remove(D);print('Deleted file: '+D);A.sendcmdline(B,'250 File deleted ok.')
			except Exception as E:print('Failed to delete file: '+str(E));A.sendcmdline(B,P)
			finally:A.closeclient()
		elif C=='MKD':
			try:D=A.get_absolute_path(F);os.mkdir(D);print('Create folder: '+D);A.sendcmdline(B,'257 Path created ok.')
			except Exception as E:print('Failed to create folder: '+str(E));A.sendcmdline(B,'550 Failed to create folder.')
			finally:A.closeclient()
		elif C=='RMD':
			try:D=A.get_absolute_path(F);os.rmdir(D);print('Deleted folder: '+D);A.sendcmdline(B,'250 Folder deleted ok.')
			except Exception as E:print(Q+str(E));A.sendcmdline(B,P)
			finally:A.closeclient()
		elif C=='CDUP':
			try:
				if A.cwd and len(A.cwd)>1:K=A.cwd.split(_A);G=_A+_A.join(K[:-1])
				else:G=_A
				os.chdir(G);A.cwd=G;print('Go to parent: '+G);A.sendcmdline(B,'250 Went to parent folder.')
			except Exception as E:print(Q+str(E));A.sendcmdline(B,'550 Failed to go to parent.')
			finally:A.closeclient()
		elif C=='RNFR':A.lastpayload=F;A.sendcmdline(B,'226 Starting rename.')
		elif C=='RNTO':
			if A.lastpayload:
				try:os.rename(A.lastpayload,F);A.sendcmdline(B,'250 Renamed file.')
				except Exception as E:print('Failed to rename file: '+str(E));A.sendcmdline(B,'550 Failed to rename file.')
				finally:A.closeclient();A.lastpayload=_B
		else:A.sendcmdline(B,'502 Unsupported command.');print('Unsupported command {} with payload {}'.format(C,F))
	def dolisten(A):
		A.isrunning=_C
		try:
			A.start_listen()
			while A.dorun:
				B,G=A.ftpsocket.accept();B.settimeout(300)
				try:
					print('FTP connection from:',G);A.sendcmdline(B,'220 Hello. Welcome to FtpTiny.')
					while A.dorun:
						E=B.readline().decode('utf-8').replace(_E,'')
						if len(E)<=0:print('Client is gone');break
						C,F=(E.split(' ')+[''])[:2];C=C.upper();print('Command={}, Payload={}'.format(C,F));A._handle_command(B,C,F);gc.collect()
				except Exception as D:print(str(D))
				finally:print('Closing dataclient socket');B.close()
		except Exception as D:print('TinyFtp error: '+str(D))
		finally:A.isrunning=_D;A.closeclient();A.datasocket.close();A.ftpsocket.close();gc.collect()
def runserver(myself):myself.dolisten()