from sqlalchemy import ForeignKey

from exts import db
from datetime import datetime

class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(100),nullable=False,unique=True)#nullable非空,unique唯一
    join_time=db.Column(db.DateTime,default=datetime.now,nullable=False)
    #性别
    sex=db.Column(db.String(1),nullable=False,default='男')
    #卡号
    card = db.Column(db.String(100),nullable=False,unique=True)
    #管理员权限
    admin=db.Column(db.Boolean,default=False)

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

class BooksModel(db.Model):
    """
    书籍模型类，用于映射数据库中的books表。
    """
    # 指定表名为books
    __tablename__ = 'books'
    # 主键，自动递增
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 书籍名称，不可为空的字符串
    Name=db.Column(db.String(50), nullable=False)
    # 书籍简介，可为空的字符串
    Synopsis=db.Column(db.String(500))
    # 作者，不可为空的字符串
    Author=db.Column(db.String(100), nullable=False)
    # 出版社，不可为空的字符串
    Publisher=db.Column(db.String(100), nullable=False)
    # 价格，不可为空的整数
    Price=db.Column(db.Integer, nullable=False)
    # 存储时间，默认为当前时间的DateTime类型
    StorageTime=db.Column(db.DateTime, default=datetime.now)
    # 书籍封面，可为空的字符串
    Cover=db.Column(db.String(100))
    StockCount = db.Column(db.Integer, nullable=False, default=0)  # 馆藏册数
    AvailableCopies = db.Column(db.Integer, nullable=False, default=0)  # 在馆册数
    BorrowedTimes = db.Column(db.Integer, nullable=False, default=0)  # 被借次数


class BorrowHistoryModel(db.Model):
    """
    借阅历史记录模型类，用于映射数据库中的borrow_history表。

    属性:
    id: 主键，自动递增的整数。
    reader_id: 外键，关联到ReaderModel的id字段，表示借阅者的ID。
    book_id: 外键，关联到BooksModel的id字段，表示被借阅书籍的ID。
    borrow_date: 借书日期，DateTime类型，默认为当前时间。
    return_date: 还书日期，DateTime类型，可为空（表示尚未归还）。

    关联关系：
    reader: 通过reader_id与ReaderModel建立一对多关系。
    book: 通过book_id与BooksModel建立一对多关系。
    """
    __tablename__ = 'borrow_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reader_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer,db.ForeignKey('books.id'), nullable=False)
    borrow_date = db.Column(db.DateTime, default=datetime.now)
    return_date = db.Column(db.DateTime, nullable=True)

    reader = db.relationship(UserModel, backref="reader_server")
    books = db.relationship(BooksModel, backref="book_file")
