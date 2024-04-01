import random

from flask import Blueprint, render_template, jsonify,redirect,url_for,session
from werkzeug.security import generate_password_hash,check_password_hash#负责用来加密密码

from exts import mail, db
from flask_mail import Message
from flask import request
import string
from models import EmailCaptchaModel,UserModel
from .forms import ReservationForm,LoginForm
from datetime import datetime

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user=UserModel.query.filter_by(email=email).first()
            if not user:
                print("邮箱不存在")
                return redirect(url_for("auth.login"))
            if check_password_hash(user.password,password):
                #cookie:
                #flask的session，是经过加密存储在浏览器的cookie中
                session['user_id'] = user.id
                return redirect("/")
            else:
                print("密码错误")
                return redirect(url_for("auth.login"))

        else:
            print(form.errors)
            return redirect(url_for("auth.login"))

@bp.route('/logout')
def logout():
    session.clear()
    return redirect("/")


@bp.route('/register',methods=['GET','POST'])
def register():
    # 验证用户提交的邮箱和验证码是否对应以及正确
    #表单验证flask-wtf:wtforms
    if request.method == 'GET':
        return render_template('register.html')
    else:
        # 验证用户提交的邮箱和验证码是否对应以及正确
        # 表单验证flask-wtf:wtforms
        form=ReservationForm(request.form)
        if form.validate():
            email=form.email.data
            username=form.username.data
            password=form.password.data
            card="US"+datetime.now().strftime("%Y%m%d")
            user=UserModel(username=username,password=generate_password_hash(password),card=card,email=email)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.register"))

# 邮箱验证码
@bp.route('/captcha/email')
def get_email_captcha():
    email = request.args.get('email')  # 获取邮箱(args参数)
    # 4/6：随机数组，字母、数字和大小写
    source = string.digits * 4
    captcha = random.sample(source, 4)
    captcha = "".join(captcha)
    message = Message('注册验证码', recipients=[email], body=f"您本次的验证码是:{captcha}")
    mail.send(message)
    # memcached/redis
    # 用数据库表的方式存储
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    # restful api
    return jsonify({"code": 200, "msg": "发送成功", "data": None})


@bp.route('/mail/test')
def mail_test():
    message = Message('邮箱测试', recipients=["865648178@qq.com"], body="这是一条测试的玩意!")
    mail.send(message)
    return "邮件发送成功"
