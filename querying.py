
from db import SessionLocal
from user.models import User,Address
from sqlalchemy.orm import join,joinedload,subqueryload,contains_eager
db = SessionLocal()

# all_users = db.query(User).all()
# first_user = db.query(User).first()
# johns = db.query(User).filter_by(first_name ="Gerald").all()
# johns_q = db.query(User).filter(User.first_name =="Gerald").all()
# gmail_users = db.query(User).filter(User.email.ilike("%@example.com")).all()
# print("Johns",johns)
# print("JohnsQ",johns_q)
# print("GMAIL_USERS",gmail_users)
# # print("all_users",all_users)
# print("first_user",first_user)

# users = db.query(User).all()   # all queries
# users = db.query(User).options(joinedload(User.addresses)).all()   #single query
# users = db.query(User).options(subqueryload(User.addresses)).all()  #2 queies
users = db.query(User)\
    .join(User.addresses)\
    .filter(Address.city == "London")\
    .options(contains_eager(User.addresses))\
    .all()

users = db.query(User)\
    .join(User.addresses)\
    .filter(Address.city == "London")\
    .options(joinedload(User.addresses))\
    .all()
 #
print("users",users)
for user in users:
    print("HI",user.addresses)




