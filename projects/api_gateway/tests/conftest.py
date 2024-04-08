import pytest
from Crypto.PublicKey import RSA
import tempfile
import os

from projects.api_gateway.src.tokens.verifier import TokenVerifier


@pytest.fixture
def given_private_key():
    return RSA.generate(1024)


@pytest.fixture
def given_public_key(given_private_key):
    return given_private_key.public_key()


@pytest.fixture
def given_private_pem(given_private_key):
    return given_private_key.export_key()


@pytest.fixture
def given_public_pem(given_public_key):
    return given_public_key.export_key()


@pytest.fixture
def given_private_pem_file(given_private_key):
    fpath = tempfile.mktemp()
    with open(fpath, "wb") as f:
        f.write(given_private_key.export_key())
    yield fpath
    os.remove(fpath)


@pytest.fixture
def given_public_pem_file(given_public_key):
    fpath = tempfile.mktemp()
    with open(fpath, "wb") as f:
        f.write(given_public_key.export_key())
    yield fpath
    os.remove(fpath)


@pytest.fixture
def given_token_verifier(given_public_pem) -> TokenVerifier:
    return TokenVerifier(given_public_pem)
