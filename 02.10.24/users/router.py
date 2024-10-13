from fastapi import Response, APIRouter, HTTPException
from users.business_logic import get_hashed_password, authenticate_user, create_access_token, get_current_user
from users.repositories import UsersRepository
from users.schemas import SAuth, SCreate

router = APIRouter(
    prefix='/auth',
    tags=['Authorization'],
)


@router.post('/register')
async def register(data: SCreate):
    is_admin = data.is_admin if data.is_admin is not None else False

    await UsersRepository.create(
        username=data.username,
        password=get_hashed_password(data.password),
        is_admin=is_admin
    )

    return {'message': 'User registered successfully'}

@router.post('/login')
async def login(data: SAuth, response: Response):
    user = await authenticate_user(data.username, data.password)
    token = create_access_token(user.id, user.is_admin)
    response.set_cookie('token', token)
    return {'token': token}

@router.get('/profile')
async def profile():
    user_id, _ = get_current_user()
    user = await UsersRepository.get_by_id(user_id)
    return {'user': user}

@router.get('/admin')
async def admin():
    user_id, is_admin = get_current_user()
    if not is_admin:
        raise HTTPException(status_code=403, detail='Admin privileges required')
    return {'message': 'Welcome admin!'}

@router.get('/user')
async def user():
    user_id, is_user = get_current_user()
    if not is_user:
        raise HTTPException(status_code=403, detail='User privileges required')
    return {'message': 'Welcome user!'}
