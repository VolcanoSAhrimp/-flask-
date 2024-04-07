# 导入所需模块和类
import json

from flask import Flask, session, g, request, jsonify
import config
from exts import db, mail
from models import UserModel
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from blueprints.admin import bp as admin_bp
from blueprints.user import bp as user_bp
from blueprints.simulation import bp as simulation_bp
from flask_migrate import Migrate
from flask_socketio import emit, SocketIO, join_room, leave_room

# 创建Flask应用实例
app = Flask(__name__)
socketio = SocketIO(app)
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
app.register_blueprint(user_bp)
app.register_blueprint(simulation_bp)


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
    return {"user": g.user}


@socketio.on('input_value')
def input_value(data):
    print(f"user_data:{data}")
    socketio.emit('input_value', {'value': data})

@socketio.on('input_book_id_value')
def input_book_id_value(data):
    print(f"book_data:{data}")
    socketio.emit('input_book_id_value', {'value': data})

# 如果作为主程序运行，运行该代码
if __name__ == '__main__':
    app.run()
