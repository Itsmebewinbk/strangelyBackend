from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from user.cruds import (
    get_all_users,
    create_user,
    delete_user_crud,
    AsyncSession,
    save_anonymous_user,
)
from db import get_sync_db, get_async_db
from user.schemas import UserCreate, GetUser, FireBaseToken
from response import ErrorResponse
from fastapi import Request

router = APIRouter()


@router.get("/items")
async def get_items():
    return {"items": ["item1", "item2"]}


@router.get("/")
async def get_users(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_async_db)
):
    return await get_all_users(db, skip=skip, limit=limit)


# @router.get("async/")
# async def get_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_sync_db)):
#     return await get_all_users(db, skip=skip, limit=limit)  # ✅ Use `await`


@router.post("/", response_model=GetUser)
def create_users(user: UserCreate, db: Session = Depends(get_sync_db)):

    try:
        return create_user(db, user)
    except ValueError as e:
        return ErrorResponse(status_code=400, detail=str(e))


@router.delete("/{id}/")
def delete_user(id: int, db: Session = Depends(get_sync_db)):
    return delete_user_crud(db, id)


@router.post("/login/")
async def login(payload: FireBaseToken, db: AsyncSession = Depends(get_async_db)):
    # request:Request
    # body = await request.json()
    # firebase_token = body.get("firebase_token")

    if not payload.firebase_token:
        return ErrorResponse(status_code=400, message="firebase_token is required")
    return await save_anonymous_user(db, payload.firebase_token)
