from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from user.models import User,ActiveToken
from user.utils import create_access_token
from user.schemas import UserCreate,Token
from datetime import datetime
from response import ErrorResponse, SuccessResponse
from sqlalchemy.future import select
from sqlalchemy import func
import uuid
from query import update_or_create_async

# templates = Jinja2Templates(directory="templates")
# jwt


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):

    if not user.password or len(user.password) < 6:
        return ErrorResponse(
            status_code=400, message="Password must be at least 6 characters long"
        )

    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        return ErrorResponse(status_code=400, message="User already exists")

    user_data = user.dict(exclude={"password"})
    user_data["profile_pic"] = (
        str(user_data["profile_pic"]) if user_data["profile_pic"] else None
    )

    try:
        new_user = User(**user_data)
        print("password", user.password)
        new_user.set_password(user.password)
        print(f"New user password (hashed): {new_user.password}")
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"Saved user password (hashed): {new_user.password}")

        return SuccessResponse(
            message="User created successfully",
            status_code=201,
            data={"id": new_user.id, "email": new_user.email},
        )

    except Exception as e:
        db.rollback()
        return ErrorResponse(status_code=500, message="Internal server error")


# def get_all_users(db: Session, skip: int = 0, limit: int = 10):
#     total_users = db.query(User).count()
#     users = db.query(User).offset(skip).limit(limit).all() if limit > 0 else []
#     response = {
#         "count": total_users,

#         "next": skip + limit if (limit > 0 and skip + limit < total_users) else None,
#         "previous": skip - limit if (limit > 0 and skip - limit >= 0) else None,
#         "results": users
#     }


async def get_all_users(db: AsyncSession, skip: int = 0, limit: int = 10):
    total_users = await db.scalar(select(func.count()).select_from(User))
    users_data = (
        await db.execute(select(User).offset(skip).limit(limit)) if limit > 0 else []
    )
    users = users_data.scalars().all()
    response = {
        "count": total_users,
        "next": skip + limit if (limit > 0 and skip + limit < total_users) else None,
        "previous": skip - limit if (limit > 0 and skip - limit >= 0) else None,
        "results": users,
    }

    return response


def delete_user_crud(db: Session, id: int):
    # delete_all_user = db.query(User).delete(synchronize_session=False)

    # print("user",user)
    user = db.get(User, id)
    if not user:
        return ErrorResponse(message="User Doesn't Exist")
    db.delete(user)
    db.commit()
    return SuccessResponse(message="User deleted Successfully")


# async def login_user(
#     db: Session, request: Request, email: str = Form(...), password: str = Form(...)
# ):

#     user = db.query(User).filter(User.email == email).first()
#     if not user or not User.verify_password(password, user.password):
#         return templates.TemplateResponse(
#             "login.html", {"request": request, "error": "Invalid credentials"}
#         )

#     request.session["user"] = {
#         "id": user.id,
#         "email": user.email,
#         "is_superuser": user.is_superuser,
#     }
#     return RedirectResponse(url="/admin", status_code=302)


async def save_anonymous_user(db: Session, firebase_token: str):
    # user = db.query(User).filter(User.firebase_token==firebase_token).first()
    result = await db.execute(select(User).where(User.firebase_token == firebase_token))
    user = result.scalars().first()
    if not user:
        try:
            password = uuid.uuid4()
            email ="anonymous@gmail.com"
            user = User(firebase_token=firebase_token,password=password,email=email)
            db.add(user)
            await db.commit()
            await db.refresh(user)
        except Exception as e:
            await db.rollback()
            return ErrorResponse(status_code=500, message="Internal server error")
        
    if user:
        try : 
            access_token = await create_access_token(data={"sub": str(user.id)})
            token, created = await update_or_create_async(
                    db,
                    ActiveToken,
                    defaults={
                        "jti": await create_access_token(data={"sub": str(user.id)}),
                        "updated_at": datetime.utcnow()
                    },
                    user_id=user.id
                )
           
           
        except Exception as e:
            await db.rollback()
            return ErrorResponse(status_code=500, message="Internal server error")

    return Token(access_token=access_token, token_type="Bearer")
