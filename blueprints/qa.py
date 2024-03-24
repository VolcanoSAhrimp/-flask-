import inspect
from pprint import pprint

from flask import Blueprint, render_template, request, g, redirect, url_for

from exts import db
from models import BooksModel,TagModel
from .forms import QuestionForm
from decorators import login_required
# import pandas as pd
bp = Blueprint('qa', __name__, url_prefix='/')


@bp.route('/')
def index():
    # questions = QuestionModel.query.order_by(QuestionModel.content_time.desc()).all()
    # books = BooksModel.query.all()
    return render_template('index.html')


@bp.route('/qa/detail/<qa_id>')
def qa_book_detail(qa_id):
    book = BooksModel.query.get(qa_id)
    return render_template('BookDetail.html', book=book)


@bp.route('/search')
def search():
    # 查询字符串的形式,/search?q=xxx
    # /search/<q>
    # post,request.from
    q = request.args.get('BookName')
    # books = QuestionModel.query.filter(QuestionModel.title.contains(q)).all()
    books = BooksModel.query.filter(BooksModel.Name.contains(q)).all()
    # data = pd.DataFrame([vars(book) for book in books])
    # print(data)
    return render_template("library-index.html", books=books)
@bp.route('/search-tag')
def search_tag():
    # 查询字符串的形式,/search?q=xxx
    # /search/<q>
    # post,request.from
    tag = request.args.get('tag_name')
    # books = QuestionModel.query.filter(QuestionModel.title.contains(q)).all()
    # books = BooksModel.query.filter(BooksModel.Name.contains(q)).all()
    books_tag = TagModel.query.filter_by(name=tag).all()
    print(books_tag)
    all_books = []
    for book in books_tag:
        all_books.extend(book.books)
    print(all_books)
    # data = pd.DataFrame([vars(book) for book in books])
    # print(data)
    return render_template("library-index.html", books=all_books)
