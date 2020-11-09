import eel
import asyncio
import threading
import socket
import Crypto

@eel.expose
def add_message(message):
	client.send(message.encode())

def listen():
	while True:
		try:
			data = client.recv(2048)
			message = data.decode()
			eel.add_message(message)()
		except:
			client.close()
			break

if __name__ == '__main__':
	eel.init('web')
	port = int(input('Введите порт: '))
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect(('127.0.0.1',8888))
	listener_task = threading.Thread(target = listen)
	listener_task.start()
	eel.start('main.html', port = port)