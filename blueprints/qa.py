from flask import Blueprint, render_template, request
from sqlalchemy.orm import aliased

from exts import db
from models import BooksModel, TagModel
from flask import Blueprint, render_template, request
from flask_sqlalchemy import pagination

from models import BooksModel, TagModel

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
    page = request.args.get('page', 1, type=int)  # 获取当前页码，默认为1
    per_page = 10  # 每页显示的数据条数
    q = request.args.get('BookName')
    books_query = BooksModel.query.filter(BooksModel.Name.contains(q))
    pagination = books_query.paginate(page=page, per_page=per_page, error_out=False)
    books = pagination.items
    return render_template("library-index.html", books=books, pagination=pagination, q=q,mode="bookName")


@bp.route('/search-tag')
def search_tag():
    page = request.args.get('page', 1, type=int)  # 获取当前页码，默认为1
    per_page = 10  # 每页显示的数据条数
    tag_name = request.args.get('tag_name')
    books = BooksModel.query.join(TagModel, BooksModel.Tags).filter(TagModel.name == tag_name).paginate(page=page, per_page=per_page, error_out=False)
    print(books.items)
    return render_template("library-index.html", books=books.items, pagination=books, q=tag_name,mode="tagName")