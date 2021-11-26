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
            'nonce': None,  # We set `None` because it's IdP initiated flow and we don't have it.
        }

    def _get_additional_payload_data(self, user: UserIdentity) -> dict:
        """
        Generate some additional payload for OpenID token.
        List of the available fields could be
            found https://openid.net/specs/openid-connect-core-1_0.html#StandardClaims .
        Any of this fields are not required and could be not used by Learnster.
        """
        return {
            'given_name': user.first_name,
            'family_name': user.last_name,
            'email': user.email,
        }
