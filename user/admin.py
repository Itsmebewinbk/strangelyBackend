# admin.py
from sqladmin import ModelView
from user.models.user import User

from fastapi import FastAPI
from datetime import datetime, timedelta

import bcrypt
from sqladmin import ModelView
from sqladmin.authentication import AuthenticationBackend
from fastapi import Request

from user.models import User
from db import get_sync_db



from sqlalchemy.orm import Session


# IMP admin login class: auto logs out the admin after 15 seconds

class AdminAuth(AuthenticationBackend):
    

    async def login(self, request: Request):
        form = await request.form()
        email = form.get("username")
        password = form.get("password")
        print("email",email)
        print("password",password)

        if not email or not password:
            return False

        email = email.strip().lower()

       
        db = next(get_sync_db())

        try:
            admin = db.query(User).filter(
                User.email == email,
                User.is_superuser == True
            ).first()
            print("admin",admin)

            if admin and admin.verify_password(password):
                print(2222222)
                request.session["user"] = {
                    "id": admin.id,
                    "email": admin.email,
                    "is_superuser": admin.is_superuser,
                }
                return True

        except Exception as e:
          
            print("Login error:", e)

        finally:
            db.close()

        return False  # invalid credentials

    async def authenticate(self, request: Request) -> bool:
        session = request.session
        if "user" in session:
            
            return True
        return False

    async def logout(self, request: Request) -> bool:
        
        request.session.clear()
        return True




class UserAdmin(ModelView, model=User):
  
    column_list = [User.id, User.first_name, User.last_name, User.email]
    
   
    column_filters = [User.first_name, User.email]
    
    
    column_searchable_list = [User.first_name, User.last_name, User.email]
    
   
    column_labels = {
        User.id: "ID",
        User.first_name: "First Name",
        User.last_name: "Last Name",
        User.email: "Email Address"
    }


