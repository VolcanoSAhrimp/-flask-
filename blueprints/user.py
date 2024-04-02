from datetime import datetime

from flask import Blueprint, render_template, request, g, redirect, url_for, jsonify
from sqlalchemy.orm import aliased

from exts import db
from models import BorrowHistoryModel, UserModel, BooksModel, TagModel

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/history_user')
def history_user():
    user_id=g.user.id
    books=UserModel.query.filter_by(id=user_id).first().reader_server
    book_his=[]
    for i in books:
        book_his.append(i.books)
        # print(i.books.id)
    return render_template("user_history.html",books=book_his)