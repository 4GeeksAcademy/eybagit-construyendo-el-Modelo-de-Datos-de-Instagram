from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    mail: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    posts: Mapped[list["Post"]] = relationship("Post", back_populates="user_rel")
    followers: Mapped[list["Follower"]] = relationship(
        "Follower",
        foreign_keys="[Follower.user_from_id]",
        back_populates="follower_rel"
    )
    following: Mapped[list["Follower"]] = relationship(
        "Follower",
        foreign_keys="[Follower.user_to_id]",
        back_populates="followed_rel"
    )
    likes: Mapped[list["Like"]] = relationship("Like", back_populates="user_rel")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="user_rel")

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "mail": self.mail,
        
        }


class Post(db.Model):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    url: Mapped[str] = mapped_column(String(250), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[str] = mapped_column(String(20), nullable=False)
    location: Mapped[str] = mapped_column(String(120), nullable=True)

    user_rel: Mapped["User"] = relationship("User", back_populates="posts")
    likes: Mapped[list["Like"]] = relationship("Like", back_populates="post_rel")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="post_rel")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "url": self.url,
            "text": self.text,
            "created_at": self.created_at,
            "location": self.location
        }


class Follower(db.Model):
    __tablename__ = "followers"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user_to_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[str] = mapped_column(String(20), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    follow_source: Mapped[str] = mapped_column(String(50), nullable=True)

    follower_rel: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user_from_id],
        back_populates="followers"
    )
    followed_rel: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user_to_id],
        back_populates="following"
    )

    def serialize(self):
        return {
            "id": self.id,
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id,
            "created_at": self.created_at,
            "is_active": self.is_active,
            "follow_source": self.follow_source
        }


class Like(db.Model):
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False)
    created_at: Mapped[str] = mapped_column(String(20), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    source: Mapped[str] = mapped_column(String(50), nullable=True)

    user_rel: Mapped["User"] = relationship("User", back_populates="likes")
    post_rel: Mapped["Post"] = relationship("Post", back_populates="likes")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "created_at": self.created_at,
            "is_active": self.is_active,
            "source": self.source
        }


class Comment(db.Model):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[str] = mapped_column(String(20), nullable=False)
    likes_count: Mapped[int] = mapped_column(Integer, nullable=False)

    user_rel: Mapped["User"] = relationship("User", back_populates="comments")
    post_rel: Mapped["Post"] = relationship("Post", back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "comment": self.comment,
            "created_at": self.created_at,
            "likes_count": self.likes_count
        }
