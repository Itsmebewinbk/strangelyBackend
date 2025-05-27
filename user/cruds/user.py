from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from user.models import User
from user.schemas import UserCreate
from fastapi import HTTPException
from response import ErrorResponse,SuccessResponse
from sqlalchemy.future import select
from sqlalchemy import func




def get_user_by_email(db:Session,email:str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
  
    if not user.password or len(user.password) < 6:
        return ErrorResponse(status_code=400, message="Password must be at least 6 characters long")
    
   
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
       return ErrorResponse(status_code=400, message="User already exists")


    
    user_data = user.dict(exclude={"password"})
    user_data["profile_pic"] = str(user_data["profile_pic"]) if user_data["profile_pic"] else None
    

    try:
        new_user = User(**user_data)
        print("password",user.password)
        new_user.set_password(user.password) 
        print(f"New user password (hashed): {new_user.password}")  
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"Saved user password (hashed): {new_user.password}")

        return SuccessResponse(
            message="User created successfully",
            status_code=201,
            data={"id": new_user.id, "email": new_user.email}
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
    users_data = await db.execute(select(User).offset(skip).limit(limit)) if limit > 0 else []
    users = users_data.scalars().all()
    response = {
        "count": total_users,
        
        "next": skip + limit if (limit > 0 and skip + limit < total_users) else None,
        "previous": skip - limit if (limit > 0 and skip - limit >= 0) else None,
        "results": users
    }
    
    return response






def delete_user_crud(db:Session,id:int):
    # delete_all_user = db.query(User).delete(synchronize_session=False)

    # print("user",user)
    user = db.get(User,id)
    if not user:
        return ErrorResponse(message="User Doesn't Exist")
    db.delete(user)
    db.commit()
    return SuccessResponse(message="User deleted Successfully")
    


