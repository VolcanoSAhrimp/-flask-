from collections import defaultdict

from flask import Blueprint, render_template, request, g

from decorators import check_user
from exts import db
from models import BorrowHistoryModel, UserModel

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/')
@check_user
def index():
    return render_template("user_base.html")


@bp.route('/history_user')
@check_user
def history_user():
    page = request.args.get('page', type=int, default=1)
    per_page = 5
    user_id = g.user.id
    borrow_histories = (
        db.session.query(BorrowHistoryModel)
        .join(UserModel, UserModel.id == BorrowHistoryModel.reader_id)
        .filter(UserModel.id == user_id)
        .order_by(BorrowHistoryModel.borrow_date.desc())
        # .all()
    )
    books=borrow_histories.paginate(page=page, per_page=per_page)
    return render_template("user_history.html", books=books.items, pagination=books,current_route="hide")


@bp.route('/user_detail')
@check_user
def user_detail():
    user_id = g.user.id
    user = UserModel.query.filter_by(id=user_id).first()
    # print(user)
    return render_template("user_detail.html", user=user)


@bp.route('/user_update')
@check_user
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
            return render_template("user_detail.html", userd=user, alert_message=message)
        except Exception as e:
            print(e)
            message = "操作失败！"
            db.session.rollback()
            return render_template("user_detail.html", userd=user, alert_message=message)
    else:
        print(f"找不到名为{username}的用户")
        return render_template("user_detail.html", userd=user)


@bp.route('/user_not_return')
@check_user
def user_not_return():
    page = request.args.get('page', type=int, default=1)
    per_page = 5
    user_id = g.user.id
    borrow_histories = (
        db.session.query(BorrowHistoryModel)
        .join(UserModel, UserModel.id == BorrowHistoryModel.reader_id)
        .filter(UserModel.id == user_id, BorrowHistoryModel.return_date.is_(None))
        .distinct(BorrowHistoryModel.book_id)
    )
    books = borrow_histories.paginate(page=page, per_page=per_page)
    return render_template("user_not_return.html", books=books.items,pagination=books, current_route="hide")
