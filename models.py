from exts import db
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)  # nullable非空,unique唯一
    join_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    # 性别
    sex = db.Column(db.String(1), nullable=False, default='男')
    # 卡号
    card = db.Column(db.String(100), nullable=False, unique=True)
    # 管理员权限
    admin = db.Column(db.Integer, default=1, nullable=False)
    # 手机号
    phone = db.Column(db.String(20))


class EmailCaptchaModel(db.Model):
    __tablename__ = 'email_captcha'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)  # unique非空
    captcha = db.Column(db.String(100), nullable=False)  # unique非空
    # used=db.Column(db.Boolean, default=False)


class TagModel(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    book_tags = db.Table("book_tags",
                         db.Column('book_id', db.Integer, db.ForeignKey('books.id'), primary_key=True),
                         db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
                         )
    # 这里还有个books属性的book表的关联关系，用于从标签查询图书


class BooksModel(db.Model):
    """
    书籍模型类，用于映射数据库中的books表。
    """
    # 指定表名为books
    __tablename__ = 'books'
    # 主键，自动递增
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 书籍名称，不可为空的字符串
    Name = db.Column(db.String(50), nullable=False)
    # 书籍简介，可为空的字符串
    Synopsis = db.Column(db.String(500))
    # 作者，不可为空的字符串
    Author = db.Column(db.String(100), nullable=False)
    # 出版社，不可为空的字符串
    Publisher = db.Column(db.String(100), nullable=False)
    # 价格，不可为空的整数
    Price = db.Column(db.Integer, nullable=False)
    # 存储时间，默认为当前时间的DateTime类型
    StorageTime = db.Column(db.DateTime, default=datetime.now)
    # 书籍封面，可为空的字符串
    Cover = db.Column(db.String(100))
    StockCount = db.Column(db.Integer, nullable=False, default=0)  # 馆藏册数
    AvailableCopies = db.Column(db.Integer, nullable=False, default=0)  # 在馆册数
    BorrowedTimes = db.Column(db.Integer, nullable=False, default=0)  # 被借次数
    Tags = db.relationship(TagModel, secondary="book_tags", backref=db.backref('books'))


class BorrowHistoryModel(db.Model):

    __tablename__ = 'borrow_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 外键关联
    reader_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)

    borrow_date = db.Column(db.Date, default=datetime.now)
    return_date = db.Column(db.Date, nullable=True)

    reader = db.relationship(UserModel, backref="reader_server")
    books = db.relationship(BooksModel, backref=db.backref('book_file', lazy='dynamic'))
