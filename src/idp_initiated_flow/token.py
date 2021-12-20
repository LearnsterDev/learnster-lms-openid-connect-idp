from calendar import timegm
from datetime import datetime, timedelta
from jwt import encode

from . import (
    keys,
    settings,
)
from .user import UserIdentity


class TokenGenerator:

    def generate_jwt(self, user: UserIdentity) -> str:
        """
        Generate valid OpenID token.
        """
        payload = self._get_auth_jwt_payload(user=user)
        payload |= self._get_additional_payload_data(user=user)

        key = keys.get_random_key()
        return encode(
            payload=payload,
            key=key.private,
            algorithm=settings.ALGORITHM,
            headers={
                'kid': key.kid,
            },
        )

    def _get_auth_jwt_payload(self, user: UserIdentity) -> dict:
        """
        Generate required payload for OpenID token.
        More info could be found https://openid.net/specs/openid-connect-core-1_0.html#IDToken .
        """
        now = datetime.utcnow()

        return {
            'iss': settings.ISSUER,
            'sub': user.email,
            'aud': settings.AUDIENCE,
            'exp': now + timedelta(minutes=2),
            'iat': now,
            'auth_time': timegm(now.utctimetuple()),  # forced to manually convert datetime to int
            'nonce': None,  # We set `None` because nonce is used for IdP initiated flows which is not valid for this use case.
        }

    def _get_additional_payload_data(self, user: UserIdentity) -> dict:
        """
        Generate additional payload for OpenID token.
        Please see this article for available fields https://openid.net/specs/openid-connect-core-1_0.html#StandardClaims
        
        Please note that the only required (and used) field is the unique user identifier field; `sub`, `email` or `oid`.
        Which user identifier field will be used depends on your SSO configuration in Learnster Studio.
        """
        return {
            'given_name': user.first_name,
            'family_name': user.last_name,
            'email': user.email,
        }
