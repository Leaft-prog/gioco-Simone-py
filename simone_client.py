import socket
import time
import tkinter as tk

root = tk.Tk()
root.title("Simone (Client)")

memoria=""
memoriatext=""

def aggiungiRosso():
	global memoria
	global memoriatext
	memoria+="1#"
	memoriatext+="rosso "
	testo.configure(text=memoriatext)
	
def aggiungiVerde():
	global memoria
	global memoriatext
	memoria+="0#"
	memoriatext+="verde "
	testo.configure(text=memoriatext)

def aggiungiBlu():
	global memoria
	global memoriatext
	memoria+="3#"
	memoriatext+="blu "
	testo.configure(text=memoriatext)

def aggiungiGiallo():
	global memoria
	global memoriatext
	memoria+="2#"
	memoriatext+="giallo "
	testo.configure(text=memoriatext)
	
def invia():
	global memoriatext
	global memoria
	s=socket.socket()
	server_address="127.0.0.1"
	server_port=12555
	try:
		s.connect((server_address, server_port))
		s.send(memoria.encode())
		messaggiodirisposta=s.recv(1024).decode()
		if(messaggiodirisposta=="0"):
			testo.configure(text="SBAGLIATO, riprova da capo")
		s.close()
		root.after(2000,cancella)

	except Exception as e:
		print(e)
	
def cancella():
	global memoria
	global memoriatext
	memoria=""
	memoriatext=""
	testo.configure(text="")

testo=tk.Label(root, width=50, text="", bg='white')

bottonerosso=tk.Button(root, width=25, height=12, bg='red', command=aggiungiRosso)
bottoneverde=tk.Button(root, width=25, height=12, bg='green', command=aggiungiVerde)
bottoneblu=tk.Button(root, width=25, height=12,bg='blue', command=aggiungiBlu)
bottonegiallo=tk.Button(root, width=25, height=12,bg='yellow', command=aggiungiGiallo)

tasto_invia=tk.Button(root, text="invia", width=25, command=invia)
tasto_cancella=tk.Button(root, text="cancella", width=25, command=cancella)

bottoneverde.grid(row=0, column=0)
bottonerosso.grid(row=0, column=1)
bottonegiallo.grid(row=1, column=0)
bottoneblu.grid(row=1, column=1)
tasto_invia.grid(row=2, column=0)
tasto_cancella.grid(row=2, column=1)
testo.grid(row=3, column=0, columnspan=2, sticky='nsew')

root.mainloop()
