import pytest
from src.presentation.api.v1.middleware.cors_middleware import CORSMiddleware

# Dummy receive
async def dummy_receive():
    return {}

@pytest.mark.asyncio
async def test_http_response_start_modifies_headers():
    sent = []

    async def mock_send(msg):
        sent.append(msg)

    async def mock_app(scope, receive, send):
        await send({'type': 'http.response.start', 'headers': [(b'x-test', b'value')]})

    middleware = CORSMiddleware(mock_app)
    await middleware({'type': 'http'}, dummy_receive, mock_send)

    headers = dict(sent[0]['headers'])
    assert headers[b'access-control-allow-origin'] == b'*'
    assert headers[b'x-test'] == b'value'

@pytest.mark.asyncio
async def test_http_response_non_start_passes_through():
    sent = []

    async def mock_send(msg):
        sent.append(msg)

    async def mock_app(scope, receive, send):
        await send({'type': 'http.response.body', 'body': b'Hello'})

    middleware = CORSMiddleware(mock_app)
    await middleware({'type': 'http'}, dummy_receive, mock_send)

    assert sent[0]['type'] == 'http.response.body'
    assert sent[0]['body'] == b'Hello'

@pytest.mark.asyncio
async def test_non_http_scope_passes_through():
    sent = []

    async def mock_send(msg):
        sent.append(msg)

    async def mock_app(scope, receive, send):
        await send({'type': 'websocket.response.start'})

    middleware = CORSMiddleware(mock_app)
    await middleware({'type': 'websocket'}, dummy_receive, mock_send)

    assert sent[0]['type'] == 'websocket.response.start'

@pytest.mark.asyncio
async def test_http_response_start_without_headers_key():
    sent = []

    async def mock_send(msg):
        sent.append(msg)

    async def mock_app(scope, receive, send):
        await send({'type': 'http.response.start'})  # no headers

    middleware = CORSMiddleware(mock_app)
    await middleware({'type': 'http'}, dummy_receive, mock_send)

    headers = dict(sent[0]['headers'])
    assert headers[b'access-control-allow-origin'] == b'*'