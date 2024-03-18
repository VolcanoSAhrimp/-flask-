from datetime import datetime

from flask import Blueprint, render_template, request, g, redirect, url_for, jsonify
from sqlalchemy.orm import aliased

from exts import db
from models import BorrowHistoryModel, UserModel, BooksModel

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
        reader_id = UserModel.query.filter(UserModel.username == username).first().id
        book_id = BooksModel.query.filter(BooksModel.Name == bookTitle).first().id
        # print(f"reader_id={reader_id.id},book_id={book_id.id}",)
        question = BorrowHistoryModel(reader_id=reader_id, book_id=book_id, borrow_date=datetime.now(),
                                      return_date=None)
        db.session.add(question)
        db.session.commit()
        return render_template('admin_borrow.html')


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
        question = BorrowHistoryModel(reader_id=reader_id, book_id=book_id, borrow_date=datetime.now(),return_date=None)
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
                          .join(history_alias,BooksModel.id == history_alias.book_id)
                          .filter(history_alias.reader_id == user.id).all())

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
    book=BorrowHistoryModel.query.filter_by(book_id=bookId,reader_id=reader_id).first()
    db.session.delete(book)
    db.session.commit()
    print(reader_id,bookId)
    return jsonify({"success":"sss"})

@bp.route('/add_book', methods=['GET','POST'])
def add_book():
    if request.method == 'GET':
        return render_template('admin_add_book.html')
    else:
        # print(request.form)
        Name=request.form.get('Name')
        Author=request.form.get('Author')
        Publisher=request.form.get('Publisher')
        Synopsis=request.form.get('Synopsis')
        Price=request.form.get('Price')
        book=BooksModel(Name=Name,Author=Author,Publisher=Publisher,Synopsis=Synopsis,Price=Price)
        db.session.add(book)
        db.session.commit()
        return jsonify({"success":"sss"})
