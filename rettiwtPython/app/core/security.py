from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext

SECRET_KEY= "MEGA_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES= 60 * 1 #* n hour

MAX_BCRYPT_BYTES = 72

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_passwd(password: str) -> str:
    """
    Password hashing function
    
    :param password: String to hash
    :type password: str
    :return: Hashed string 
    :rtype: str
    """
    truncated = password.encode("utf-8")[:MAX_BCRYPT_BYTES]
    return pwd_context.hash(truncated.decode("utf-8"))

def verify_passwd(plain: str, hashed: str) -> bool:
    """
    Hash verification function
    
    :param plain: Plain string to verify
    :type plain: str
    :param hashed: Hashed string to verify
    :type hashed: str
    :return: If are equal
    :rtype: bool
    """
    truncated = plain.encode("utf-8")[:MAX_BCRYPT_BYTES]
    return pwd_context.verify(truncated.decode("utf-8"), hashed)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Bearer token creation function
    
    :param data: Dictionary containing the token data
    :type data: dict
    :param expires_delta: Expiration date of the token
    :type expires_delta: Optional[timedelta]
    """
    to_encode = data.copy()
    expire= datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token:str):
    """
    Token decoding function
    
    :param token: Token string
    :type token: str
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        return None
    
    