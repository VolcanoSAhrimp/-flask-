from datetime import datetime

from flask import Blueprint, render_template, request, g, redirect, url_for, jsonify
from sqlalchemy.orm import aliased

from exts import db
from models import BorrowHistoryModel, UserModel, BooksModel, TagModel

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/')
def index():
    return render_template("user_base.html")


@bp.route('/history_user')
def history_user():
    user_id = g.user.id
    books = UserModel.query.filter_by(id=user_id).first().reader_server
    book_his = []
    for i in books:
        book_his.append(i.books)
        # print(i.books.id)
    return render_template("user_history.html", books=book_his, current_route="hide")


@bp.route('/user_detail')
def user_detail():
    user_id = g.user.id
    user = UserModel.query.filter_by(id=user_id).first()
    # print(user)
    return render_template("user_detail.html", user=user)


@bp.route('/user_update')
def user_update():
    id = request.args.get('id')
    username = request.args.get('username')
    email = request.args.get('email')
    sex = request.args.get('sex')
    admin = request.args.get('admin')
    user = UserModel.query.filter_by(id=id).first()
    if user:
        user.username = username
        user.email = email
        user.sex = sex
        user.admin = admin
        user.email = email
        # 提交数据库事务
        try:
            db.session.commit()
            message = "操作成功！"
            return render_template("user_detail.html", user=user, alert_message=message)
        except Exception as e:
            print(e)
            message = "操作失败！"
            db.session.rollback()
            return render_template("user_detail.html", user=user, alert_message=message)
    else:
        print(f"找不到名为{username}的用户")
        return render_template("user_detail.html", user=user)
