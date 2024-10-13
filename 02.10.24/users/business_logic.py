from datetime import datetime, timedelta
from fastapi import Request, Depends
from fastapi import HTTPException
from jose import jwt, ExpiredSignatureError
from passlib.context import CryptContext

from users.repositories import UsersRepository

password_context = CryptContext(schemes=["bcrypt"],deprecated='auto')


def get_hashed_password(password):
    return password_context.hash(password)


def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)




def get_token(request:Request):
    token = request.headers.get('Authorization')
    if token is None:
        token = request.cookies.get('token')
    if token is None:
        raise HTTPException(status_code=401, detail='Token not found')
    return token

def create_access_token(user_id: int, is_admin: bool):
    expired_at = datetime.utcnow() + timedelta(hours=2)
    token = jwt.encode({
        'exp': expired_at,
        'user_id': user_id,
        'is_admin': is_admin
    }, 'secret_key')
    return token

async def authenticate_user(username: str, password: str):
    user = await UsersRepository.get_by_id(username)
    if user is None:
        raise HTTPException(status_code=401, detail='Incorrect username')
    if verify_password(password, user.hashed_password):
        return user
    raise HTTPException(status_code=401, detail='Incorrect password')

def get_current_user(token=Depends(get_token)):
    try:
        decoded_token = jwt.decode(token, 'secret_key')
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token expired')
    user_id = decoded_token['user_id']
    is_admin = decoded_token.get('is_admin', False)
    return user_id, is_admin


