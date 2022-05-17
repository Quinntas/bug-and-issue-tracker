import base64
import datetime
import hashlib
import json

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from passlib.hash import pbkdf2_sha256

hkdf = HKDF(
    algorithm=hashes.SHA256(),  # You can swap this out for hashes.MD5()
    length=32,
    salt=None,  # You may be able to remove this line but I'm unable to test
    info=None,  # You may also be able to remove this line
    backend=default_backend()
)

PEPER = 'oSJposJdpfojspdOJSFPdojfpsODJFPSODJFpsodjfPOSJDfposJDFPOSJDFPSOEFPOjsepofj'
FERNET_KEY = 'AOoijqOIjdaoimd0!@N)1m0239j109kASImd09wkdp(KpmOP!kP)(DKapkdmapijwadim'
FERNET = Fernet(base64.urlsafe_b64encode(hkdf.derive(bytes(PEPER + FERNET_KEY, 'utf-8'))))


def encrypt_sha265(content: str) -> str:
    encoded_string = (PEPER + content).encode()
    return hashlib.sha256(encoded_string).hexdigest()


def gen_pbkdf2_sha256(content: str) -> str:
    return pbkdf2_sha256.hash(PEPER + content)


def verify_encryption(in_content: str, db_content: str) -> bool:
    return pbkdf2_sha256.verify(PEPER + in_content, db_content)


def encrypt_fernet(message: str) -> str:
    message = bytes(message, 'utf-8')
    return FERNET.encrypt(message).decode()


def decrypt_fernet(message: str) -> str:
    message = bytes(message, 'utf-8')
    return FERNET.decrypt(message).decode()


def verify_access_token(token: str) -> bool:
    if token is None:
        return False
    try:
        token = json.loads(decrypt_fernet(token))
    except (json.JSONDecodeError, InvalidToken):
        return False
    expiration_date = datetime.datetime.strptime(token['expiration_date'], "%d/%m/%Y-%H:%M:%S")
    if (expiration_date - datetime.datetime.utcnow()).total_seconds() <= 0:
        return False
    return True


def gen_access_token(class_id: str) -> tuple | str:
    expiration_date = (datetime.datetime.utcnow() + datetime.timedelta(days=15)).strftime(
        "%d/%m/%Y-%H:%M:%S")

    token = {
        "expiration_date": expiration_date,
        "id": class_id
    }

    access_token = encrypt_fernet(json.dumps(token))

    return access_token, expiration_date
