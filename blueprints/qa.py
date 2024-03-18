import inspect
from pprint import pprint

from flask import Blueprint, render_template, request, g, redirect, url_for

from exts import db
from models import BooksModel
from .forms import QuestionForm, AnswerForm
from decorators import login_required

bp = Blueprint('qa', __name__, url_prefix='/')


@bp.route('/')
def index():
    # questions = QuestionModel.query.order_by(QuestionModel.content_time.desc()).all()
    # books = BooksModel.query.all()
    return render_template('index.html')


@bp.route('/qa/public', methods=['GET', 'POST'])
@login_required
def public_qa():
    if request.method == 'GET':
        return render_template('public_question.html')
    else:
        form = QuestionForm(request.form)
        # print(f"form: {form.data}")
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            return redirect("/")
        else:
            print(form.errors)
            return redirect(url_for('qa.public_qa'))


@bp.route('/qa/detail/<qa_id>')
def qa_book_detail(qa_id):
    book = BooksModel.query.get(qa_id)
    return render_template('BookDetail.html', book=book)


@bp.route('/answer/public', methods=['POST'])
def answer_public():
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        answer = AnswerModel(content=content, question_id=question_id, author_id=g.user.id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for('qa.qa_detail', qa_id=question_id))

    else:
        print(form.errors)
        return redirect(url_for('qa.qa_detail', qa_id=request.form.get("question_id")))


@bp.route('/search')
def search():
    # 查询字符串的形式,/search?q=xxx
    # /search/<q>
    # post,request.from
    q = request.args.get('BookName')
    # books = QuestionModel.query.filter(QuestionModel.title.contains(q)).all()
    books = BooksModel.query.filter(BooksModel.Name.contains(q)).all()
    return render_template("library-index.html", books=books)
