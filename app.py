# 导入所需模块和类
from flask import Flask,session,g
import config
from exts import db,mail
from models import UserModel
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from blueprints.admin import bp as admin_bp
from flask_migrate import Migrate

# 创建Flask应用实例
app = Flask(__name__)

# 绑定配置文件
app.config.from_object(config)

# 初始化数据库
db.init_app(app)
mail.init_app(app)

# 创建数据库迁移对象
migrate = Migrate(app, db)

# 注册蓝图
app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)

@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, 'user', user)
    else:
        setattr(g, 'user', None)

@app.context_processor
def my_context_processor():
    return {"user":g.user}

# 如果作为主程序运行，运行该代码
if __name__ == '__main__':
    app.run()
