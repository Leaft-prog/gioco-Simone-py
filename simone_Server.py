import time
import socket
import pygame
import threading
import sys
import random
import os

class serverThread (threading.Thread):
	def __init__(self, indirizzoIP, porta):
		threading.Thread.__init__(self)
		self.indirizzoIP=indirizzoIP
		self.porta=porta

	def run(self):
		self.s=socket.socket()
		self.s.bind((self.indirizzoIP, self.porta))
		self.s.listen(5)
		self.cicloDiAscolto()

	def cicloDiAscolto(self):
		global azionidaFare
		global stop_event
		global azionidaFareLock
		global azionigiocatore
		global azionigiocatoreLock
		global stato
		global statoLock
		while not stop_event.is_set():
			try:
				conn, addr=self.s.accept()
				dato=conn.recv(1024).decode()
				statoLock.acquire()
				if(stato==2):
					azionigiocatoreLock.acquire()
					if not dato:
						conn.close()
						statoLock.release()
						azionigiocatoreLock.release()
						continue
					azionigiocatore = [int(x) for x in dato.split("#") if x]
					self.controllo(conn)
					azionigiocatoreLock.release()
					stato=3
				statoLock.release()
				conn.close()
			except Exception as e:
				print(e)

	def controllo(self, conn):
		azionidaFareLock.acquire()
		if(azionigiocatore!=azionidaFare):
			conn.send("0".encode())
		else:
			conn.send("1".encode())
		azionidaFareLock.release()


class generatore(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		self.ciclo()


	def ciclo(self):
		global statoLock
		global stop_event
		global stato
		while not stop_event.is_set():
			statoLock.acquire()
			if(stato==0):
				self.generaAzioni()
				stato=1
			statoLock.release()
			time.sleep(1)


	def generaAzioni(self):
		global azionidaFare
		global azionidaFareLock

		azionidaFareLock.acquire()
		azionidaFare.append(random.randint(0,3))
		azionidaFareLock.release()




class pygameThread(threading.Thread):
	def __init__(self, serverSocket):
		threading.Thread.__init__(self)
		self.serverSocket=serverSocket

	def run(self):
		pygame.init()
		self.finestra=pygame.display.set_mode((800,800))
		pygame.display.set_caption("Simone (Server)")
		self.fillcolor=(0,0,0)
		self.rosso=(100,0,0)
		self.verde=(0,100,0)
		self.blu=(0,0,100)
		self.giallo=(100,100,0)
		self.rossoAcceso=(255,0,0)
		self.verdeAcceso=(0,255,0)
		self.bluAcceso=(0,0,255)
		self.gialloAcceso=(255,255,0)
		self.cicloDisegno()

	def cicloDisegno(self):
		global azionigiocatore
		global azionigiocatoreLock
		global azionidaFare
		global azionidaFareLock
		global stato
		global stop_event
		global statoLock

		while not stop_event.is_set():
			self.finestra.fill(self.fillcolor)
			statoLock.acquire()
			st=stato
			statoLock.release()
			if(st==1):
				azionidaFareLock.acquire()
				pygame.time.delay(1000)
				for x in azionidaFare:
					if(x==0):
						pygame.draw.rect(self.finestra, self.verdeAcceso, (0,0, 400,400))
					else:
						pygame.draw.rect(self.finestra, self.verde, (0,0,400,400))
					if(x==2):
						pygame.draw.rect(self.finestra, self.gialloAcceso, (0,400,400,400))
					else:
						pygame.draw.rect(self.finestra, self.giallo, (0,400,400,400))
					if(x==1):
						pygame.draw.rect(self.finestra, self.rossoAcceso, (400,0,400,400))
					else:
						pygame.draw.rect(self.finestra, self.rosso, (400,0,400,400))
					if(x==3):
						pygame.draw.rect(self.finestra, self.bluAcceso, (400,400,400,400))
					else:
						pygame.draw.rect(self.finestra, self.blu, (400,400,400,400))
					pygame.display.update()
					pygame.time.delay(1000)
					pygame.draw.rect(self.finestra, self.verde, (0,0,400,400))
					pygame.draw.rect(self.finestra, self.giallo, (0,400,400,400))
					pygame.draw.rect(self.finestra, self.rosso, (400,0,400,400))
					pygame.draw.rect(self.finestra, self.blu, (400,400,400,400))
					pygame.display.update()
					pygame.time.delay(500)

				azionidaFareLock.release()
				statoLock.acquire()
				stato=2
				statoLock.release()
			elif(st==3):
				azionigiocatoreLock.acquire()
				pygame.time.delay(1000)
				self.controllo()
				pygame.time.delay(1000)
				azionigiocatoreLock.release()
				statoLock.acquire()
				stato=0
				statoLock.release()
			else:
				pygame.draw.rect(self.finestra, self.verde, (0,0,400,400))
				pygame.draw.rect(self.finestra, self.giallo, (0,400,400,400))
				pygame.draw.rect(self.finestra, self.rosso, (400,0,400,400))
				pygame.draw.rect(self.finestra, self.blu, (400,400,400,400))
				pygame.display.update()



			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					self.serverSocket.s.close()
					stop_event.set()
					pygame.quit()
					os._exit(0)
					break

			pygame.time.delay(10)
			


	def controllo(self):
		if azionidaFare != azionigiocatore:
			azionidaFare.clear()
			azionigiocatore.clear()
			pygame.draw.rect(self.finestra, self.verdeAcceso, (0,0,400,400))
			pygame.draw.rect(self.finestra, self.gialloAcceso, (0,400,400,400))
			pygame.draw.rect(self.finestra, self.rossoAcceso, (400,0,400,400))
			pygame.draw.rect(self.finestra, self.bluAcceso, (400,400,400,400))
			pygame.display.update()
		else:
			azionigiocatore.clear()

azionidaFare=[]
azionidaFareLock=threading.Lock()
azionigiocatore=[]
stato=0
statoLock=threading.Lock()
azionigiocatoreLock=threading.Lock()

stop_event = threading.Event()

server=serverThread("127.0.0.1", 12555)
gen=generatore()
pyg=pygameThread(server)

server.start()
gen.start()
pyg.start()


server.join(timeout=1)
gen.join(timeout=1)
pyg.join(timeout=1)
