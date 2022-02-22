# OpenID Connect IdP Example (for JWT based autentication)

A basic example of an OpenID Connect IdP implementation for JWT based authentication.
Please use this as a base for your own implementation and make sure to read relevant OpenID and JWT documenation. 


### Example of a valid OpenID token generation flow:
1. The user clicks a "Login to Learnster" button in the third party system/interface.
2. The third party client (frontend) calls their `/token` endpoint to fetch a valid OpenID token for the user.
For an example of an `/token` enpoint, please see https://github.com/Learnster/openid-connect-idp/blob/main/src/idp_initiated_flow/token.py

3. The third party client (frontend) makes an in browser request to Learnster's OpenID login endpoint.
4. Learnster requests a `/keys` endpoint from the third party to fetch a list of public keys and verifies the OpenID token.
5. Learnster completes the authentication process (validates the token etc.) and returns a 302 redirect (the redirect target is Learnster's frontend).
6. The third party frontend receives the redirect response from Learnster's OpenID login endpoint and redirects the user's browser to the redirect location.

#### To support a JWT based authentication flow you will need to:  
1. Provide a `/keys` endpoint with valid public keys.  
2. Provide a `/token` endpoint that generates valid OpenID tokens (naturally, since this is an internal endpoint you can name it whatever you see fit).  
3. Call your `/token` endpoint to get a token for the user, then call Learnster's OpenID login endpoint to get a redirect location and redirect your user to that location.  

### Example project

Only IdP initiated flows are relevant for these use cases. See below for instructions how to set up the example project:

Requires Python 3.6+. Developed with Python 3.9.2.

Usage

1. Install dependencies `pip install -r requirements.txt`.

2. Generate public/private keys:

    2.1 Generate RSA keys with a suitable tool. You could also use `keys_generation.py` module.   
   ```python
   from src.idp_initiated_flow.keys_generation import generate_rsa_key, key_to_string
   
   key = generate_rsa_key()
   private, public = key_to_string(key)
   
   with open('./private.pem', mode='w') as f:
       f.write(private)
   
   with open('./public.pem', mode='w') as f:
       f.write(public)
   ```
   
   2.2 Export required ENV variables:
   ```shell
   export PRIVATE_KEY=`cat ./private.pem`
   export PUBLIC_KEY=`cat ./public.pem`
   export KEY_KID='any-unique-string'
   ```
   
3. Run application `uvicorn src.idp_initiated_flow.main:app --reload`.

4. Replace constants with your learnster instance constants:

   4.1 `idp_initiated_flow/settings.py:ISSUER`  
   4.2 `idp_initiated_flow/settings.py:AUDIENCE`  
   4.3 `idp_initiated_flow/html/index.html:learnster_url`  

5. Request `http://127.0.0.1:8000/keys` for keys endpoint and `http://127.0.0.1:8000/index`.
