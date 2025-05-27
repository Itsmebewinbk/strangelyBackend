# from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
# from sqlalchemy.orm import Relationship
# from datetime import datetime
# from db import Base
# from passlib.context import CryptContext
# from sqlalchemy.orm import Mapped, mapped_column, relationship

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# class TimeStampModel(Base):
#     __abstract__ = True
#     created_at = Column(DateTime, default=datetime.utcnow())
#     updated_at = Column(DateTime, onupdate=datetime.utcnow())


# class User(TimeStampModel):
#     __tablename__ = "users"
#     id: Mapped[int] = mapped_column(primary_key=True, unique=True)
#     profile_pic: Mapped[str] = mapped_column(
#         String(500),
#         nullable=True,
#     )
#     # profile_pic = Column(String(500), nullable=True)
#     first_name: Mapped[str] = mapped_column(index=True, nullable=True)
#     last_name: Mapped[str] = mapped_column(index=True, nullable=True)

#     email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
#     password: Mapped[str] = mapped_column(String, nullable=False)
#     # preference = Relationship(
#     #     "Preference", back_populates="user", uselist=False, passive_deletes=True
#     # )
#     # addresses = Relationship("Address", back_populates="user", passive_deletes=True)
#     # roles = Relationship("Role", secondary="user_roles",back_populates="user",passive_deletes=True)

#     # Relationships using declarative base
#     preference: Mapped["Preference"] = relationship(
#         "Preference", back_populates="user", uselist=False, passive_deletes=True
#     )
#     addresses: Mapped[list["Address"]] = relationship(
#         "Address", back_populates="user", passive_deletes=True
#     )
#     roles: Mapped[list["Role"]] = relationship(
#         "Role", secondary="user_roles", back_populates="users", passive_deletes=True
#     )

#     def set_password(self, password: str):

#         if password:

#             self.password = pwd_context.hash(password)  #
#         else:
#             print("Received empty password!")

#     def verify_password(self, password: str) -> bool:
#         """Verify a given password against the stored hash."""
#         return pwd_context.verify(password, self.password)

#     def __repr__(self):
#         return f"{self.__class__.__name__}, name:{self.first_name}"


# # ONE TO ONE
# class Preference(TimeStampModel):
#     __tablename__ = "preferences"

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     language = Column(String(80), nullable=False)
#     currency_code = Column(String(3), nullable=False)
#     user_id = Column(
#         Integer,
#         ForeignKey("users.id", ondelete="CASCADE"),
#         nullable=False,
#         index=True,
#         unique=True,
#     )
#     user = Relationship("User", back_populates="preference")


# # ONE TO MANY


# class Address(TimeStampModel):
#     __tablename__ = "addresses"

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     road_name = Column(String(80), nullable=False)
#     post_code = Column(String(80), nullable=False)
#     city = Column(String(80), nullable=False)
#     user_id = Column(
#         Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
#     )
#     user = Relationship("User", back_populates="addresses")

#     def __repr__(self):
#         return f"{self.__class__.__name__}, name:{self.city}"


# # M2M
# class Role(Base):
#     __tablename__ = "roles"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(80), nullable=False)
#     slug = Column(String(80), nullable=False, unique=True)
#     user = Relationship(
#         "User", secondary="user_roles", back_populates="roles", passive_deletes=True
#     )

#     def __repr__(self):
#         return f"{self.__class__.__name__},name:{self.name}"


# class UserRole(Base):
#     __tablename__ = "user_roles"

#     user_id = Column(
#         Integer,
#         ForeignKey("users.id", ondelete="CASCADE"),
#         primary_key=True,
#     )
#     role_id = Column(
#         Integer,
#         ForeignKey("roles.id", ondelete="CASCADE"),
#         primary_key=True,
#     )
