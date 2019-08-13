#!/usr/bin/env python

import asyncio
import websockets
import asyncpg

class App(object):

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.ws_list = []
        self.conn = None
        self.q = None

    async def ws_handler(self, ws, path):
        def listener(*args):
            self.q.put_nowait(args)
        self.ws_list.append(ws)
        if self.q is None:
            self.q = asyncio.Queue(loop=self.loop)
        if self.conn is None:
            self.conn = await asyncpg.connect(user='testuser', password='12345', database='pgws', host='127.0.0.1')
            await self.conn.add_listener('todo_updates', listener)
        print('new socket!!!')
        while True:
            item = await self.q.get()
            if item is not None:
                for ws in self.ws_list:
                    await ws.send(item[3])
            await asyncio.sleep(1)

if __name__ == '__main__':
    app = App()
    start_server = websockets.serve(app.ws_handler, 'localhost', 8080)
    app.loop.run_until_complete(start_server)
    app.loop.run_forever()