from exts import db
from datetime import datetime

class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(100),nullable=False,unique=True)#unique非空
    join_time=db.Column(db.DateTime,default=datetime.now,nullable=False)

class EmailCaptchaModel(db.Model):
    __tablename__ = 'email_captcha'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100),nullable=False)#unique非空
    captcha = db.Column(db.String(100),nullable=False)#unique非空
    # used=db.Column(db.Boolean, default=False)

class QuestionModel(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text, nullable=False)
    content_time = db.Column(db.DateTime, default=datetime.now)

    #外键
    author_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship(UserModel,backref="questions")

class AnswerModel(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(100), nullable=False)
    created_time = db.Column(db.DateTime, default=datetime.now)

    #外键
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    question = db.relationship(QuestionModel,backref=db.backref("answers",order_by=created_time.desc))
    author = db.relationship(UserModel,backref="authors")
