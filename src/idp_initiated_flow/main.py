"""
Example of valid OpenID token generation.

Flow:
    1. User request `/index` page in browser and press button "Login to Learnster".
    2. FE request `/token` endpoint and receive OpenID token for this user.
    3. FE make in browser request to Learnster OpenID login endpoint.
    4. Learnster check OpenID token and request `/keys` endpoint to fetch list of public keys.
    5. Learnster complete authentication process and return 302 redirect to Learnster FE.
    6. FE receive redirect response from Learnster OpenID login endpoint and redirect user browser to Location.
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
