#!/usr/bin/env python

# WS server example

import asyncio
import http
import websockets
import pgpubsub
import queue
#from multiprocessing import Process, Queue
#import threading

#def f(q):
#    q.put(pubsub.get_event())

#async def get_event(q):
#    return q.get()

pgresq = asyncio.Queue()

def start_pgthread(loop):
    loop.create_task(coro_pgthread(loop))

async def coro_pgthread(loop):
    await loop.run_in_executor(None, pgthread_main, pgresq, loop)

def pgthread_main(qout, loop):
    pubsub = pgpubsub.connect(user='protonic', password='geheim', database='pgws')
    pubsub.listen('todo_updates')
    while True:
        e = pubsub.get_event()
        if e is not None:
            loop.call_soon_threadsafe(qout.put_nowait, e.payload)

async def ws_handler(ws, path):
    print('new socket!!!')
    loop = asyncio.get_event_loop()
    while True:
        #e = await get_event(q) 
        p = await pgresq.get()
        await ws.send(p)
    return ws

#pubsub = pgpubsub.connect(user='protonic', password='geheim', database='pgws')
#pubsub.listen('todo_updates')
#q = Queue()
#p = Process(target=f, args=(q,))
#p.start()
#p.join()
#x = threading.Thread(target=f, args=(q,))
#x.start
loop = asyncio.get_event_loop()
start_pgthread(loop)
start_server = websockets.serve(ws_handler, 'localhost', 8766)
loop.run_until_complete(start_server)
loop.run_forever()
