"""
Example of RSA key generation.
"""
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey


def generate_rsa_key() -> RSAPrivateKey:
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
    )

    return private_key


def key_to_string(private_key: RSAPrivateKey) -> tuple[str, str]:
    public_key_str = (
        private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('ascii')
    )

    private_key_str = (
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ).decode('ascii')
    )

    return private_key_str, public_key_str
