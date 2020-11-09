import asyncio
import json

users = []

async def broadcast(message, nickname, exclude = []):
	for user in users:
		if(user not in exclude):
			user[1].write(json.dumps({'nickname':nickname, 'message':message}).encode())
			await user[1].drain()

async def handler(reader, writer):
	test = True
	try:
		writer.write(json.dumps({'nickname':'', 'message':'Введите свое имя'}).encode())
		await writer.drain()
		new_nick = await reader.read(2048)
		new_nick = new_nick.decode().replace('\n','')
		new_user = [reader,writer,new_nick]
		users.append(new_user)
		writer.write(json.dumps({'nickname':'', 'message':'Добропожаловать на сервер'}).encode())
		await writer.drain()
	except:
		test = False
		writer.close()
	if(test):
		broadcast_task = asyncio.create_task(broadcast(f'Пользователь {new_nick} присоединилсь','',[new_user]))
		await asyncio.gather(broadcast_task)
		while True:
			try:
				data = await reader.read(2048)
				message = data.decode().replace('\n','')
			except:
				break
			broadcast_task = asyncio.create_task(broadcast(message,new_nick,[]))
			await asyncio.gather(broadcast_task)
		broadcast_task = asyncio.create_task(broadcast(f'Пользователь {new_nick} покинул беседу','',[new_user]))
		await asyncio.gather(broadcast_task)
		users.remove(new_user)
		writer.close()

async def main():
	server = await asyncio.start_server(handler, '127.0.0.1',8888)
	addr = server.sockets[0].getsockname()
	print(f'Server listening on {addr}')
	await server.serve_forever()

if __name__ == '__main__':
	asyncio.run(main())