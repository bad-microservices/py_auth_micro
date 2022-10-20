from dataclasses import dataclass
from cryptography.hazmat.primitives.asymmetric.types import PRIVATE_KEY_TYPES
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from ..Core import SignMethod
from typing import Union


class TokenConfig:
    default_sign_method: SignMethod
    hs_secret: Union[str, None]
    public_key_path: Union[str, None]
    private_key_path: Union[str, None]
    private_key: Union[bytes, PRIVATE_KEY_TYPES, None] = None
    public_key: Union[bytes, None] = None

    def __init__(
        self,
        *,
        default_sign_method: SignMethod,
        hs_secret: Union[str, None] = None,
        public_key_path: Union[str, None] = None,
        private_key_path: Union[str, None] = None,
        private_key_secret: Union[bytes, None] = None
    ):

        self.default_sign_method = default_sign_method
        self.hs_secret = hs_secret
        self.public_key_path = public_key_path
        self.private_key_path = private_key_path

        if private_key_path is not None:
            self.private_key = _load_key_from_file(private_key_path, private_key_secret)

        if public_key_path is not None:
            self.public_key = _load_key_from_file(private_key_path, None)

    def __repr__(self):
        values=[
            f"default_sign_method={self.default_sign_method!r}",
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
