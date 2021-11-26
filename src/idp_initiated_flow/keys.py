import random
from dataclasses import dataclass
from typing import Sequence

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.types import (
    PRIVATE_KEY_TYPES,
    PUBLIC_KEY_TYPES,
)

from . import settings


@dataclass
class Key:
    public: PUBLIC_KEY_TYPES
    private: PRIVATE_KEY_TYPES
    kid: str


def get_keys() -> Sequence[Key]:
    """
    Return all available keys to sign OpenID token.

    Check OpenID spec and consider signing and keys rotation policies required for your organization.
    https://openid.net/specs/openid-connect-core-1_0.html#SigEnc
    """
    return [
        Key(public=_load_public_key(settings.PUBLIC_KEY),
            private=_load_private_key(settings.PRIVATE_KEY),
            kid=settings.KEY_KID),
    ]


def get_random_key() -> Key:
    """
    Get single key to sign OpenID token.
    """
    keys = get_keys()
    return random.choice(keys)


def _load_private_key(private_key: str) -> PRIVATE_KEY_TYPES:
    return serialization.load_pem_private_key(
        private_key.encode('utf8'),
        password=None,
    )


def _load_public_key(public_key: str) -> PUBLIC_KEY_TYPES:
    return serialization.load_pem_public_key(
        public_key.encode('utf8'),
    )
