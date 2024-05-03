# from werkzeug.security import generate_password_hash,check_password_hash#负责用来加密密码
# print(generate_password_hash("sCFg5846"))
from eralchemy import render_er
render_er(Base, 'erd_from_sqlalchemy.png')