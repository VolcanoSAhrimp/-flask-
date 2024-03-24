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


# @bp.route('/qa/public', methods=['GET', 'POST'])
# @login_required
# def public_qa():
#     if request.method == 'GET':
#         return render_template('public_question.html')
#     else:
#         form = QuestionForm(request.form)
#         # print(f"form: {form.data}")
#         if form.validate():
#             title = form.title.data
#             content = form.content.data
#             question = QuestionModel(title=title, content=content, author=g.user)
#             db.session.add(question)
#             db.session.commit()
#             return redirect("/")
#         else:
#             print(form.errors)
#             return redirect(url_for('qa.public_qa'))


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
    for book in books_tag:
        books=book.books
    print(books)
    # data = pd.DataFrame([vars(book) for book in books])
    # print(data)
    return render_template("library-index.html", books=books)
