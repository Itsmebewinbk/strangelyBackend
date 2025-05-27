from db import Base
from user.models import TimeStampModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Enum, Integer,event
from enum import Enum
from sqlalchemy import Enum as SQLEnum
# from user.models import User

class ChatTypeChoices(Enum):
    CHAT = 0
    GROUP = 1


class Chat(TimeStampModel):
    __tablename__ = "chats"
    id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, primary_key=True, unique=True
    )
    chat_type: Mapped[ChatTypeChoices] = mapped_column(
        SQLEnum(ChatTypeChoices), default=ChatTypeChoices.CHAT
    )
    # members : Mapped[list["Member"]] = relationship(
    #     "Member",back_populates="chat",passive_deletes=True
    # )
    members : Mapped[list["Member"]] = relationship(
        "Member",back_populates="chat", cascade="all, delete"
    )
    name : Mapped[str] = mapped_column(
        String(800),nullable=True,
    )
    image : Mapped[str] = mapped_column(
        String(2000),nullable=True
    )

   

class Member(Base):
    __tablename__ = "members"
    id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, primary_key=True, unique=True
    )
    chat_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("chats.id", ondelete="CASCADE"), nullable=False
    )
    chat : Mapped["Chat"] = relationship("Chat",back_populates="members")
    user_id : Mapped["User"]=mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
   
    user : Mapped["User"] = relationship("User",back_populates="members",lazy="selectin")

    def __repr__(self):
        return f"Chat id : {self.chat_id}"
    



class Message(TimeStampModel):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, primary_key=True, unique=True
    )
    text: Mapped[str] = mapped_column(
        String(500),nullable=True,
    )
    file: Mapped[str]

