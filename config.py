#加密密钥
SECRET_KEY = 'dksjtcihujurnu'

# 数据库配置信息
hostname = "127.0.0.1"
post = 3306
username = "root"
password = "123456"
database = "database_learn"
db_url = f"mysql+pymysql://{username}:{password}@{hostname}:{post}/{database}?charset=utf8mb4"
SQLALCHEMY_DATABASE_URI = db_url

# 邮箱配置信息
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "mail"
MAIL_PASSWORD = "mail_password"
MAIL_DEFAULT_SENDER = "mail"