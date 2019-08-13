#!/usr/bin/env python

import asyncio
import asyncpg
from aiohttp import web
import aiohttp_jinja2
import jinja2
import os 

class WSHandler:

    def __init__(self):
        self.ws_list = []
        self.conn = None
        self.q = None

    @aiohttp_jinja2.template('index.html')
    async def index(self,request):
        return {}

    async def websocket_handler(self, request):
        def listener(*args):
            self.q.put_nowait(args)
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        self.ws_list.append(ws)
        print('new socket!!!')
        if self.q is None:
            self.q = asyncio.Queue()
        if self.conn is None:
            self.conn = await asyncpg.connect(user='testuser', password='12345', database='pgws', host='127.0.0.1')
            await self.conn.add_listener('todo_updates', listener)
        while True:
            item = await self.q.get()
            if item is not None:
                for ws1 in self.ws_list:
                    await ws1.send_str(item[3])
            await asyncio.sleep(1)

if __name__ == '__main__':
    handler = WSHandler()
    app = web.Application()
    app.router.add_get('/', handler.index)
    app.router.add_get('/ws', handler.websocket_handler)
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(os.path.dirname(os.path.realpath(__file__))))
    web.run_app(app)