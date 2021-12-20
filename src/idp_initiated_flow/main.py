"""
Example of a valid OpenID token generation flow:

1. The user clicks a "Login to Learnster" button in the third party system/interface.
2. The third party client (frontend) calls their `/token` endpoint to fetch a valid OpenID token for the user.
For an example of an `/token` enpoint, please see https://github.com/Learnster/openid-connect-idp/blob/main/src/idp_initiated_flow/token.py

3. The third party client (frontend) makes an in browser request to Learnster's OpenID login endpoint.
4. Learnster requests a `/keys` endpoint from the third party to fetch a list of public keys and verifies the OpenID token.
5. Learnster completes the authentication process (validates the token etc.) and returns a 302 redirect (the redirect target is Learnster's frontend).
6. The third party frontend receives the redirect response from Learnster's OpenID login endpoint and redirects the user's browser to the redirect location.

To sum up:

a. You will need to provide a `/keys` endpoint with valid public keys.
b. You will need to provide a `/token` endpoint that generates valid OpenID tokens (naturally, since this is an internal endpoint you can name it whatever you see fit).
c. You will call your `/token` endpoint to get a token for the user, then call Learnster's OpenID login endpoint to get a redirect location and redirect your user to that location.
"""

import base64

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

from .keys import get_keys
from .token import TokenGenerator
from .user import get_user_identity
from .settings import KEYS_TYPE
from .utils import get_bytes_length

app = FastAPI()


@app.get('/index')
async def index_endpoint() -> HTMLResponse:
    with open('./src/idp_initiated_flow/html/index.html') as f:
        content = f.read()

    return HTMLResponse(content)


@app.post('/token')
async def token_endpoint() -> JSONResponse:
    user = get_user_identity()
    jwt = TokenGenerator().generate_jwt(user=user)
    return JSONResponse({'token': jwt})


@app.get('/keys')
async def keys_endpoint() -> JSONResponse:
    keys = get_keys()
    serializer_keys = []
    for key in keys:
        public_numbers = key.public.public_numbers()

        key_data = {
            'kty': KEYS_TYPE,
            'use': 'sig',
            'kid': key.kid,
            'n': base64.urlsafe_b64encode(int.to_bytes(public_numbers.n,
                                                       length=get_bytes_length(public_numbers.n),
                                                       byteorder='big')).decode('utf8'),
            'e': base64.urlsafe_b64encode(int.to_bytes(public_numbers.e,
                                                       length=get_bytes_length(public_numbers.e),
                                                       byteorder='big')).decode('utf8'),
            # Could also include `x5t` and `x5c` values,
            # but they are not required by Learnster and skipped in this example
        }
        serializer_keys.append(key_data)

    data = {
        'keys': serializer_keys,
    }

    return JSONResponse(content=data, status_code=200)
