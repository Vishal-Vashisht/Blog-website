from config.logger_handler import logger
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Text

migrate = Migrate()
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    users_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String, nullable=False)
    userposts = db.relationship("Posts", back_populates="user")
    usercomments = db.relationship("Comments", back_populates="user")
    userliked = db.relationship("Likes", back_populates="user")

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.exception(str(e))

    @classmethod
    def create_new_user(cls, *args):
        new_user = cls(username=args[0], password=args[1])
        new_user.save()
        return new_user


class Posts(db.Model):
    __tablename__ = "posts"

    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    users_id = db.Column(db.Integer, db.ForeignKey("users.users_id"),
                         nullable=False)
    post_content = db.Column(db.String, nullable=False)
    likes = db.Column(db.Integer, server_default="0", nullable=False)
    created_date = db.Column(db.DateTime(timezone=True),
                             server_default=db.func.now())

    postlikes = db.relationship("Likes", back_populates="posts")
    postcomments = db.relationship("Comments", back_populates="posts")

    user = db.relationship("User", back_populates='userposts')

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.exception(str(e))

    @classmethod
    def create_post(cls, post_content, created_by):
        new_post = cls(post_content=post_content, users_id=created_by)
        new_post.save()
        return new_post


class Comments(db.Model):
    __tablename__ = "comments"

    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    post_id = db.Column(db.Integer, db.ForeignKey("posts.post_id"),
                        nullable=False)

    comment = db.Column(Text, nullable=False)

    comment_date = db.Column(db.DateTime(timezone=True),
                             server_default=db.func.now())

    comment_by = db.Column(
        db.Integer, db.ForeignKey("users.users_id"),
        nullable=False)

    posts = db.relationship("Posts", back_populates='postcomments')
    user = db.relationship("User", back_populates='usercomments')


class Likes(db.Model):
    __tablename__ = "likes"

    like_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.post_id"),
        nullable=False
        )
    liked_by = db.Column(
        db.Integer, db.ForeignKey("users.users_id"),
        nullable=False)

    posts = db.relationship("Posts", back_populates="postlikes")
    user = db.relationship("User", back_populates='userliked')

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.exception(str(e))

    def delete_(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.exception(str(e))

    @classmethod
    def post_liked(cls, post_id, user_id):
        new_like = cls(post_id=post_id, liked_by=user_id)
        new_like.save()
        return new_like


class Logs(db.Model):
    __tablename__ = "Logs"
    __bind_key__ = "pg_sql1"

    logid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    details = db.Column(db.Text)
    created_date = db.Column(
        db.DateTime(timezone=True),
        server_default=db.func.now()
        )

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.exception(str(e))

    @classmethod
    def create_log(cls, log_data):
        log = cls(details=log_data)
        log.save()


class Migrations:
    def __init__(self):
        try:
            logger.info("Creating table..")
            db.create_all()
            logger.info("success")
        except Exception as e:
            logger.info(f"Failed : {str(e)}")
