from dataclasses import dataclass
from abc import ABC, abstractmethod
from cryptography.hazmat.primitives.asymmetric.types import PRIVATE_KEY_TYPES
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from typing import Union

from ..Core import SignMethod

class TokenConfig:
    default_sign_method: SignMethod
    allowed_sign_methods: list[SignMethod]
    issuer: str
    symetric_secret: Union[str,None]
    public_key: Union[bytes,None]
    private_key: Union[bytes, PRIVATE_KEY_TYPES]
    public_key_path: Union[str,None]
    private_key_path: Union[str,None]

    def encode_secret(self,method:SignMethod) -> Union[bytes,PRIVATE_KEY_TYPES,str]:
        if method is SignMethod.HS256 or method is SignMethod.HS384 or method is SignMethod.HS512:
            return self.symetric_secret
        return self.private_key

    def decode_secret(self,method:SignMethod) -> Union[bytes,str]:
        if method is SignMethod.HS256 or method is SignMethod.HS384 or method is SignMethod.HS512:
            return self.symetric_secret
        return self.public_key

    def __init__(
        self,
        *,
        default_sign_method: SignMethod,
        allowed_sign_methods: list[SignMethod],
        issuer: str,
        symetric_secret: Union[str,None] = None,
        public_key_path: Union[str,None] = None,
        private_key_path: Union[str,None] = None,
        private_key_secret: Union[bytes, None] = None,
    ):
        if symetric_secret is None and (public_key_path is None or private_key_path is None):
            raise ValueError("you must either specify an symetric secret or a a public/private key pair")

        self.default_sign_method = default_sign_method
        self.allowed_sign_methods = allowed_sign_methods
        self.issuer = issuer
        self.symetric_secret = symetric_secret
        self.public_key_path = public_key_path
        self.private_key_path = private_key_path

        if private_key_path is not None:
            self.private_key = _load_key_from_file(private_key_path, private_key_secret)

        if public_key_path is not None:
            self.public_key = _load_key_from_file(private_key_path, None)


    def __repr__(self):
        values = [
            f"issuer={self.issuer!r}",
            f"default_sign_method={self.default_sign_method!r}",
            f"sign_methods={self.sign_methods!r}",
            f"hs_secret={self.hs_secret!r}",
            f"public_key_path={self.public_key_path!r}",
            f"private_key_path={self.private_key_path!r}",
        ]

        return f"TokenConfig({', '.join(values)})"


def _load_key_from_file(
    keypath: str, secret: bytes = None
) -> Union[bytes, PRIVATE_KEY_TYPES]:

    with open(keypath, "rb") as keyfile:
        keybytes = keyfile.read()

    # if no secret was specified we assume that returning the bytes is enough
    if secret is None:
        return keybytes

    return serialization.load_pem_private_key(
        keybytes, password=secret, backend=default_backend()
    )
