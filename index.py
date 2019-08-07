#!/usr/bin/env python

# WS server example

import asyncio
import http
import websockets
import pgpubsub

pubsub = pgpubsub.connect(user='protonic', password='geheim', database='pgws')
pubsub.listen('todo_updates')

"""
async def health_check(path, request_headers):
    if path == "/health/":
        return http.HTTPStatus.OK, [], b"OK\n"
"""

async def echo(ws, path):
    """
    async for message in websocket:
        await websocket.send(message)
    """
    for e in pubsub.events(yield_timeouts=True):
        if e is None:
            #ws.send_frame('', ws.OPCODE_PING)
            pass
        else:
            print(e)
            await ws.send(e.payload)

start_server = websockets.serve(echo, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
