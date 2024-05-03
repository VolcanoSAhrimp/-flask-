import os
from datetime import datetime

from flask import Blueprint, render_template, request, jsonify, current_app
from sqlalchemy import not_
from sqlalchemy.orm import aliased
from werkzeug.utils import secure_filename

from decorators import check_admin, check_root
from exts import db
from models import BorrowHistoryModel, UserModel, BooksModel, TagModel

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/index')
@check_admin
def index():
    return render_template('admin_borrow.html')


# 图书出借
@bp.route('/lend_book', methods=['GET', 'POST'])
@check_admin
def lend_book():
    if request.method == 'GET':
        return render_template('admin_borrow.html')
    else:
        form = request.form
        username = form.get('username')
        card = form.get('libraryCardNo')
        bookid = form.get('bookID')
        print(bookid)
        bookTitle = form.get('bookTitle')
        # 查询当前图书的借阅状态
        existing_loan = (
            BorrowHistoryModel.query
            .filter(BorrowHistoryModel.book_id == bookid, BorrowHistoryModel.return_date.is_(None))
            .first()
        )
        if existing_loan:
            # 图书已被借出且未归还，返回警告信息
            return render_template('admin_borrow.html', alert_message="该图书已被借出，尚未归还！")
        # 查询读者信息
        reader_book_info = (
            db.session.query(
                UserModel.id.label('reader_id'),
                BooksModel.id.label('book_id')
            )
            .join(BooksModel, BooksModel.id == bookid)
            .filter(UserModel.username == username)
            .first()
        )
        reader_id = reader_book_info.reader_id
        book_id = reader_book_info.book_id
        # 添加新的借阅记录
        new_loan = BorrowHistoryModel(
            reader_id=reader_id,
            book_id=book_id,
            borrow_date=datetime.now(),
            return_date=None
        )
        db.session.add(new_loan)
        db.session.commit()
        # 成功借阅，返回正常页面（传递 alert_message）
        return render_template('admin_borrow.html', alert_message="图书借阅成功！")


@bp.route('/return_book', methods=['GET', 'POST'])
@check_admin
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
        cover_image = request.files['CoverImage']
        if cover_image:
            filename = secure_filename(cover_image.filename)  # 使用安全的文件名
            cover_image.save(os.path.join(current_app.root_path, 'static/images', filename))  # 保存到images文件夹
            Cover = filename  # 将保存后的文件名赋值给变量Cover
        else:
            Cover = None  # 如果未上传封面，则设置为None
        book = BooksModel(Name=Name, Author=Author, Publisher=Publisher, Synopsis=Synopsis, Price=Price,Cover=Cover)
        db.session.add(book)
        db.session.commit()
        return render_template('admin_add_book.html', message="图书添加成功")


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
            return jsonify({'tags': []})


@bp.route('/add_tags', methods=['GET', 'POST'])
@check_admin
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
@check_admin
def list_book():
    page = request.args.get('page', type=int, default=1)
    per_page = 15  # 每页显示的数据条数，可以根据需要调整
    search_query = request.args.get('q', type=str, default='')  # 获取搜索关键词

    if search_query:
        books = BooksModel.query.filter(
            BooksModel.Name.ilike(f'%{search_query}%') |
            BooksModel.Author.ilike(f'%{search_query}%')
        ).paginate(page=page, per_page=per_page)
    else:
        books = BooksModel.query.paginate(page=page, per_page=per_page)

    return render_template('list_book.html', books=books.items, pagination=books, current_route="hide")


@bp.route('/book_detail/<int:book_id>')
@check_admin
def book_detail(book_id):
    book = BooksModel.query.filter_by(id=book_id).first()
    return render_template("update_book_detail.html", book=book)


@bp.route('/update_book', methods=['POST'])
def update_book():
    q = request
    id = q.form.get('id')
    name = q.form.get('bookName')
    Publisher = q.form.get('Publisher')
    Synopsis = q.form.get('Synopsis')
    Author = q.form.get('Author')
    Price = q.form.get('Price')
    book = BooksModel.query.filter_by(id=id).first()
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


@bp.route('/admin_user_purview')
@check_root
def admin_user_purview():
    page = request.args.get('page', type=int, default=1)
    per_page = 20  # 每页显示的数据条数，可以根据需要调整
    search_query = request.args.get('q', type=str, default='')  # 获取搜索关键词
    # 筛除 root 用户并根据搜索关键词过滤
    query = UserModel.query.filter(not_(UserModel.username == 'root'))
    if search_query:
        query = query.filter(
            UserModel.username.ilike(f'%{search_query}%') |
            UserModel.email.ilike(f'%{search_query}%')
        )
    users = query.paginate(page=page, per_page=per_page)
    return render_template('admin_user_purview.html', users=users.items, pagination=users, current_route='hide')


@bp.route('/admin_user_detail/<int:user_id>')
@check_root
def admin_user_detail(user_id):
    user = UserModel.query.filter_by(id=user_id).first()

    return render_template('admin_user_detail.html', user_admin=user)


@bp.route('/user_update')
@check_root
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
            return render_template("admin_user_detail.html", user_admin=user, alert_message=message)
        except Exception as e:
            print(e)
            message = "操作失败！"
            db.session.rollback()
            return render_template("admin_user_detail.html", user_admin=user, alert_message=message)
    else:
        print(f"找不到名为{username}的用户")
        return render_template("admin_user_detail.html", user_admin=user)


@bp.route('/admin_user_borrow', methods=['GET', 'POST'])
@check_root
def admin_user_borrow():
    return render_template('admin_user_brrow_detail.html', tags=TagModel.query.all())


@bp.route('/admin_user_book_list', methods=['GET', 'POST'])
@check_root
def admin_user_book_list():
    filtered_books = []
    if request.method == 'POST':
        search_type = request.form.get('search_type')
        search_value = request.form.get('search_value').strip()
        selected_tags = request.form.getlist('tags[]')
        selected_tags = [int(tag) for tag in selected_tags]
        borrow_start = request.form.get('borrow_start')
        if borrow_start:
            borrow_start = datetime.fromisoformat(borrow_start).date()
        else:
            # 处理空值情况，如设置默认值、抛出异常、返回错误提示等
            borrow_start = None  # 示例：设置为None或默认日期
        borrow_end = request.form.get('borrow_end')
        if borrow_end:
            borrow_end = datetime.fromisoformat(borrow_end).date()
        else:
            # 处理空值情况，如设置默认值、抛出异常、返回错误提示等
            borrow_end = None  # 示例：设置为None或默认日期
        return_start = request.form.get('return_start')
        if return_start:
            return_start = datetime.fromisoformat(return_start).date()
        else:
            # 处理空值情况，如设置默认值、抛出异常、返回错误提示等
            return_start = None  # 示例：设置为None或默认日期
        return_end = request.form.get('return_end')
        if return_end:
            return_end = datetime.fromisoformat(return_end).date()
        else:
            # 处理空值情况，如设置默认值、抛出异常、返回错误提示等
            return_end = None  # 示例：设置为None或默认日期
        # 根据搜索条件构造查询
        query = UserModel.query
        if search_type == 'username':
            query = query.filter(UserModel.username.contains(search_value))
        elif search_type == 'card':
            query = query.filter(UserModel.card.contains(search_value))
        user = query.first()
        filtered_books = []
        for book in user.reader_server:
            tags=[]
            if selected_tags:
                tags = [i.id for i in book.books.Tags]
                if not any(tag in selected_tags for tag in tags):  # 反转条件，保留包含指定标签的书
                    continue

            if all([borrow_start, borrow_end]):
                bor = book.borrow_date
                if not borrow_start <= bor <= borrow_end:
                    continue

            if all([return_start, return_end]):
                retu = book.return_date
                if retu is not None:
                    if not return_start <= retu <= return_end:
                        continue
            filtered_books.append(book)

    else:
        filtered_books = []
    print(filtered_books)
    return render_template('admin_user_book_list.html', users=filtered_books,target=user)
