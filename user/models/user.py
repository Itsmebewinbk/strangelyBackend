from sqlalchemy import Integer, String, DateTime, ForeignKey, Enum, Boolean, text
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from datetime import datetime
from passlib.context import CryptContext
from db import Base
import enum, jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TimeStampModel(Base):
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class AuthMethodEnum(str, enum.Enum):
    GOOGLE = "google"
    EMAIL = "email"
    APPLE = "apple"


class DeviceTypeEnum(str, enum.Enum):
    ANDROID = "android"
    IOS = "ios"
    WEB = "web"


class GenderEnum(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class User(TimeStampModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    profile_pic: Mapped[str] = mapped_column(String(500), nullable=True)
    first_name: Mapped[str] = mapped_column(String, index=True, nullable=True)
    last_name: Mapped[str] = mapped_column(String, index=True, nullable=True)
    firebase_token: Mapped[str] = mapped_column(String, index=True)
    authentication_method: Mapped[AuthMethodEnum] = mapped_column(
        Enum(AuthMethodEnum), nullable=True
    )
    device_type: Mapped[str] = mapped_column(Enum(DeviceTypeEnum), nullable=True)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("0")  
    )
    gender: Mapped[GenderEnum] = mapped_column(
        Enum(GenderEnum), default=GenderEnum.OTHER
    )
    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("0")
    )
    is_registered: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("0") 
    )
    password: Mapped[str] = mapped_column(String, nullable=False)

    # One-to-One relationship
    preference: Mapped["Preference"] = relationship(
        "Preference",
        back_populates="user",
        uselist=False,
        passive_deletes=True,
    )

    # One-to-Many relationship
    addresses: Mapped[list["Address"]] = relationship(
        "Address", back_populates="user", passive_deletes=True
    )

    # Many-to-Many relationship
    roles: Mapped[list["Role"]] = relationship(
        "Role",
        secondary="user_roles",
        back_populates="users",
        passive_deletes=True,
    )

    # members: Mapped[list["Member"]] = relationship(
    #     "Member", back_populates="user", cascade="all, delete-orphan"
    # )

    def set_password(self, password: str):
        if password:
            self.password = pwd_context.hash(password)
        else:
            print("Received empty password!")

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password)

    def __repr__(self):
        return f"User(id={self.id}, email={self.email}, name={self.first_name})"


# (One-to-One with User)
class Preference(TimeStampModel):
    __tablename__ = "preferences"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    language: Mapped[str] = mapped_column(String(80), nullable=False)
    currency_code: Mapped[str] = mapped_column(String(3), nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    user: Mapped["User"] = relationship("User", back_populates="preference")


class ActiveToken(TimeStampModel):
    __tablename__ = "active_token"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    jti: Mapped[str] = mapped_column(
        String,
        nullable=False,  #
        unique=True,
    )


# (One-to-Many with User)
class Address(TimeStampModel):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    road_name: Mapped[str] = mapped_column(String(80), nullable=False)

    city: Mapped[str] = mapped_column(String(80), nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"Address(city={self.city})"


#  (Many-to-Many with User)
class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    slug: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)

    users: Mapped[list["User"]] = relationship(
        "User",
        secondary="user_roles",
        back_populates="roles",
        passive_deletes=True,
    )

    def __repr__(self):
        return f"Role(name={self.name})"


#  User-Role association table (Many-to-Many)
class UserRole(Base):
    __tablename__ = "user_roles"

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    role_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True
    )
