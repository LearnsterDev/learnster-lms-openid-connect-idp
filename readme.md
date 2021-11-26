# OpenID Connect IdP Example

Very basic example of OpenID Connect IdP.

Currently include implementation only for IdP initiated flow.

Require Python3.6+. Developed with Python3.9.2

Usage

1. Install dependencies `pip install -r requirements.txt`.

2. Generate public/private keys:

    2.1 Generate RSA key with any tool. You could also use `keys_generation.py` module.   
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
