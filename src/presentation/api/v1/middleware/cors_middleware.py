
class CORSMiddleware:
    
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope['type'] == 'http':
            async def send_wrapper(message):
                if message['type'] == 'http.response.start':
                    headers = dict(message.get('headers', []))
                    headers[b'access-control-allow-origin'] = b'*'
                    headers[b'access-control-allow-methods'] = b'GET, POST, PUT, DELETE, OPTIONS'
                    headers[b'access-control-allow-headers'] = b'Authorization, Content-Type'
                    message['headers'] = list(headers.items())
                await send(message)

            await self.app(scope, receive, send_wrapper)
        else:
            await self.app(scope, receive, send)
