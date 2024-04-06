from datetime import datetime

from flask import Blueprint, render_template, request, g, redirect, url_for, jsonify
from sqlalchemy.orm import aliased

from exts import db
from models import BorrowHistoryModel, UserModel, BooksModel, TagModel
from pandas import DataFrame

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/index')
def index():
    return render_template('admin_borrow.html')


# 图书出借
@bp.route('/lend_book', methods=['GET', 'POST'])
def lend_book():
    if request.method == 'GET':
        return render_template('admin_borrow.html')
    else:
        form = request.form
        username = form.get('username')
        card = form.get('libraryCardNo')
        bookid = form.get('bookID')
        bookTitle = form.get('bookTitle')
        reader_book_info = (
            db.session.query(
                UserModel.id.label('reader_id'),
                BooksModel.id.label('book_id')
            )
            .join(BooksModel, BooksModel.Name == bookTitle)
            .filter(UserModel.username == username)
            .first()
        )
        reader_id = reader_book_info.reader_id
        book_id = reader_book_info.book_id
        history = BorrowHistoryModel.query.filter_by(reader_id=reader_id, book_id=book_id).first()
        if history and history.return_date:
            # 如果存在借阅历史且已借出，返回警告信息
            return render_template('admin_borrow.html', alert_message="你已经借出去，尚未归还！")
        else:
            question = BorrowHistoryModel(
                reader_id=reader_id,
                book_id=book_id,
                borrow_date=datetime.now(),
                return_date=None
            )
            db.session.add(question)
            db.session.commit()

            # 成功借阅，返回正常页面（可选择性地传递 alert_message）
            return render_template('admin_borrow.html', alert_message="图书借阅成功！")


@bp.route('/return_book', methods=['GET', 'POST'])
def return_book():
    if request.method == 'GET':
        return render_template('admin_return.html')
    else:
        form = request.form
        username = form.get('username')
        card = form.get('libraryCardNo')
        bookid = form.get('bookID')
        bookTitle = form.get('bookTitle')
        reader_id = UserModel.query.filter(UserModel.username == username).first().id
        book_id = BooksModel.query.filter(BooksModel.Name == bookTitle).first().id
        # print(f"reader_id={reader_id.id},book_id={book_id.id}",)
        question = BorrowHistoryModel(reader_id=reader_id, book_id=book_id, borrow_date=datetime.now(),
                                      return_date=None)
        db.session.add(question)
        db.session.commit()
        return render_template('admin_borrow.html')


@bp.route('/search_name', methods=['POST'])
def search_name():
    library_card_no = request.form.get('libraryCardNo')
    # print(library_card_no)
    if library_card_no:
        try:
            username = UserModel.query.filter(UserModel.card == library_card_no).first().username
            # print(username)
            return jsonify({'username': username})
        except:
            return jsonify({'username': ''})
    else:
        try:
            bookId = request.form.get('bookID')
            bookTitle = BooksModel.query.filter(BooksModel.id == bookId).first().Name
            print(bookTitle)
            return jsonify({'bookTitle': bookTitle})
        except:
            return jsonify({'bookTitle': ''})


@bp.route('/search_book', methods=['POST'])
def search_book():
    library_card_no = request.form.get('libraryCardNo')
    # 首先根据卡号查询用户ID
    user = UserModel.query.filter_by(card=library_card_no).first()

    if user:
        # 创建一个别名以方便查询关联的借阅历史记录
        history_alias = aliased(BorrowHistoryModel)

        # 根据用户ID查询该用户的借阅历史记录并关联到对应的书籍信息
        borrowed_books = (db.session.query(BooksModel)
                          .join(history_alias, BooksModel.id == history_alias.book_id)
                          .filter(history_alias.reader_id == user.id,
                                  history_alias.return_date.is_(None))
                          # .filter(history_alias.return_date==None)
                          .all())

        # 转换为 JSON 格式返回给前端
        book_list = [{'book_id': book.id, 'title': book.Name} for book in borrowed_books]
        print(book_list)
        return jsonify({'books': book_list})
    else:
        return jsonify({'error': '未找到对应卡号的用户'}), 404


@bp.route('/del_book', methods=['POST'])
def del_book():
    library_card_no = request.form.get('libraryCardNo')
    bookId = request.form.get('bookId')
    reader_id = UserModel.query.filter_by(card=library_card_no).first().id
    book = BorrowHistoryModel.query.filter_by(book_id=bookId, reader_id=reader_id, return_date=None).first()
    book.return_date = datetime.now()
    db.session.commit()
    print(reader_id, bookId)
    return jsonify({"success": "sss"})


@bp.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'GET':
        return render_template('admin_add_book.html')
    else:
        # print(request.form)
        Name = request.form.get('Name')
        Author = request.form.get('Author')
        Publisher = request.form.get('Publisher')
        Synopsis = request.form.get('Synopsis')
        Price = request.form.get('Price')
        book = BooksModel(Name=Name, Author=Author, Publisher=Publisher, Synopsis=Synopsis, Price=Price)
        db.session.add(book)
        db.session.commit()
        return jsonify({"success": "sss"})


@bp.route('/search_tags', methods=['GET', 'POST'])
def search_tags():
    if request.method == 'GET':
        return render_template('add_tags.html')
    else:
        try:
            bookId = request.form.get('bookID')
            # print(bookId)
            book = BooksModel.query.filter_by(id=bookId).first()
            bookName = book.Name
            # print(bookName)
            tags = book.Tags
            # print(tags)
            tags = [{'id': tag.id, 'name': tag.name} for tag in tags]
            # print(tags)
            return jsonify({"books": bookName, "tags": tags})
        except:
            return jsonify({"books": bookName, 'tags': []})


@bp.route('/add_tags', methods=['GET', 'POST'])
def add_tags():
    if request.method == 'GET':
        return render_template('add_tags.html')
    else:
        tag = request.form.get('add-tag')
        flg = TagModel.query.filter_by(name=tag).first()
        bookId = request.form.get('bookID')
        book = BooksModel.query.filter_by(id=bookId).first()
        print(flg)
        if not flg:
            tags = TagModel(name=tag)
            db.session.add(tags)
            db.session.commit()
            flg1 = TagModel.query.filter_by(name=tag).first()
            book.Tags.append(flg1)
        else:
            book.Tags.append(flg)
        db.session.add(book)
        db.session.commit()
        return render_template('add_tags.html')


@bp.route('/list_book', methods=['GET', 'POST'])
def list_book():
    books = BooksModel.query.filter_by().all()
    print(books)
    return render_template('list_book.html', books=books, current_route="hide")


@bp.route('/book_detail/<int:book_id>')
def book_detail(book_id):
    # q = request.args.get('book_id')
    # book = BooksModel.query.filter_by(id=q).first()
    book = BooksModel.query.filter_by(id=book_id).first()
    # print(book.Name)
    # data=DataFrame([vars(book_data) for book_data in book])
    # print(data)
    return render_template("update_book_detail.html", book=book)


@bp.route('/update_book', methods=['POST'])
def update_book():
    q = request
    # print(q)
    id = q.form.get('id')
    print(id)
    name = q.form.get('bookName')
    Publisher = q.form.get('Publisher')
    Synopsis = q.form.get('Synopsis')
    Author = q.form.get('Author')
    Price = q.form.get('Price')
    # Publisher = q.args.get('Publisher')
    book = BooksModel.query.filter_by(id=id).first()
    # print(book)
    # 更新记录
    if book:
        book.Name = name
        book.Synopsis = Synopsis
        book.Author = Author
        book.Price = Price
        book.Publisher = Publisher

        # 提交数据库事务（如果你使用的是支持事务的ORM，如SQLAlchemy）
        db.session.commit()
        return jsonify({"success": "sss"})
    else:
        print(f"找不到名为《{name}》的图书")
        return jsonify({"error": "sss"})
    # return jsonify({"books": bookName, 'tags': []})


@bp.route('/del_tag')
def del_tag():
    tagId = request.args.get('tag_id')
    bookId = request.args.get('book_id')
    # print(tagId,bookId)
    tag = TagModel.query.filter_by(id=tagId).first()
    book = BooksModel.query.filter_by(id=bookId).first()
    try:
        tag.books.remove(book)
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()  # 出现错误时回滚事务
        print(f"An error occurred: {e}")
        return jsonify({"error": False})
