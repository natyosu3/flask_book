from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

from flask_sqlalchemy.model import Model
from flask_login import UserMixin
from apps.app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash


# db.Modelを継承したUserクラスを作成する
class User(db.Model, Model, UserMixin):
    # テーブル名を指定する
    __tablename__ = "users"
    # カラムを定義する
    id = Column(Integer, primary_key=True)
    username = Column(String, index=True, unique=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


    # パスワードをリセットするためのプロパティ
    @property
    def password(self):
        raise AttributeError("読み取り不可")
    
    # パスワードをセットするためのセッター関数でハッシュ化したパスワードをセットする
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    # パスワードをチェックする
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # メールアドレス重複チェックをする
    def is_duplicate_email(self):
        return User.query.filter_by(email=self.email).first() is not None
    

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)