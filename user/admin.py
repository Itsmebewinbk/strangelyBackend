# admin.py
from sqladmin import ModelView
from user.models.user import User

from fastapi import FastAPI



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


