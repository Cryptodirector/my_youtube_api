from sqlalchemy import ForeignKey
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from app.main.database import Base


class Video(Base):
    __tablename__ = "video"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    link: Mapped[str] = mapped_column(nullable=False)
    id_user: Mapped[int] = mapped_column(ForeignKey('user.id'))


class Comments(Base):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(1000), nullable=False)
    id_video: Mapped[int] = mapped_column(ForeignKey('video.id'), nullable=False)
    id_user: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
