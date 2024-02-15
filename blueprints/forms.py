import wtforms
from flask_wtf import FlaskForm
from wtforms.validators import Email, Length, EqualTo, InputRequired
from models import UserModel, EmailCaptchaModel
from exts import db


# Form:主要来验证前端提交的数据是否符合要求
class ReservationForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误，请重输")])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message="验证码长度为4位，请重输")])
    username = wtforms.StringField(validators=[Length(min=3, max=20, message="用户名长度在3-20位，请重输")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码长度在6-20位，请重输")])
    password_confirm = wtforms.StringField(validators=[EqualTo('password', message="密码输入不一致，请重输")])

    # 自定义验证
    # 邮箱是否被注册
    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError("该邮箱已被注册，请更换邮箱")

    # 验证码是否正确
    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        print(EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first())
        if not captcha_model:
            raise wtforms.ValidationError(message="验证码错误，请重试")
        # else:
        #     # todo: 可以删掉captcha_model，因为后面不会用到
        #     db.session.delete(captcha_model)
        #     db.session.commit()


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误，请重输")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码长度在6-20位，请重输")])


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=3, max=100, message="标题格式错误，请重输")])
    content = wtforms.StringField(validators=[Length(min=1, message="内容格式错误，请重输")])


class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[Length(min=1, message="内容格式错误，请重输")])
    question_id = wtforms.IntegerField(validators=[InputRequired(message="必须传入问题id")])
