from simple_websocket_server import WebSocketServer, WebSocket

debug = True


class SimpleChat(WebSocket):
    def handle(self):
        if debug:
            print(self.data)
        for client in clients:
            if client != self:
                client.send_message(self.data)

    def connected(self):
        clients.append(self)
        if debug:
            print(self.address, 'connected')

    def handle_close(self):
        clients.remove(self)
        if debug:
            print(self.address, 'closed')


clients = []

server = WebSocketServer('', 8000, SimpleChat)
server.serve_forever()
