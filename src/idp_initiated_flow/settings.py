import os

PUBLIC_KEY = os.environ.get('PUBLIC_KEY')
PRIVATE_KEY = os.environ.get('PRIVATE_KEY')
KEY_KID = os.environ.get('KEY_KID')

# Name of IdP service
ISSUER = os.environ.get('ISSUER', 'idp.com')
AUDIENCE = os.environ.get('AUDIENCE', '<instance-name>.learnster.com')

ALGORITHM = 'RS256'  # Feel free to use any kind of `RS` or `PS` algorithm
KEYS_TYPE = 'RSA'
