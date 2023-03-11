#!/usr/bin/env python3
import asyncio
import shlex
from cowsay import COW_PEN, list_cows, cowsay

clients = {}
available_logins = set(list_cows(COW_PEN))
free_logins = set(list_cows(COW_PEN))
clients_login = {}


async def chat(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(me)
    clients[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())
    command = ""
    while not reader.at_eof() and command != "exit":
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())

                request = q.result().decode().strip()
                command = shlex.split(request)[0]
                command_args = shlex.split(request)[1:]
                if command == "login":
                    cow_type = command_args[0]
                    if cow_type in available_logins:
                        if cow_type not in clients_login.values():
                            free_logins.remove(cow_type)
                            clients_login[me] = cow_type
                            await clients[me].put(f"Success login as {cow_type}")
                        else:
                            await clients[me].put(f"Login {cow_type} already in use")
                    else:
                        await clients[me].put(f"unknown login {cow_type}")
                elif command == "who":
                    await clients[me].put('\n'.join(clients_login.values()))
                elif command == "cows":
                    await clients[me].put('\n'.join(free_logins))
                elif command == "yield":
                    if me in clients_login:
                        for out in clients.values():
                            if out is not clients[me]:
                                cow_message = cowsay(command_args[0], cow=clients_login[me])
                                await out.put(cow_message)
                    else:
                        await clients[me].put(f"Not authorized can't send any messages to other clients!")
                elif command == "say":
                    if me in clients_login:
                        if command_args[0] in clients_login.values():
                            for key in clients:
                                if clients_login[key] == command_args[0]:
                                    cow_message = cowsay(command_args[1], cow=clients_login[me])
                                    await clients[key].put(cow_message)
                        else:
                            await clients[me].put(f"There is no client with login {command_args[0]}!")
                    else:
                        await clients[me].put(f"Not authorized can't send any messages to other clients!")
                elif command == "exit":
                    break
                else:
                    for out in clients.values():
                        if out is not clients[me]:
                            await out.put(f"{me} {q.result().decode().strip()}")
            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
    send.cancel()
    receive.cancel()
    print(me, "DONE")
    del clients[me]
    if me in clients_login:
        free_logins.add(clients_login[me])
        del clients_login[me]
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
