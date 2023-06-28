from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

from apps.app import db
from werkzeug.security import generate_password_hash


# db.Modelを継承したUserクラスを作成する
class User(db.Model):
    # テーブル名を指定する
    __tablename__ = "users"
    # カラムを定義する
    id = Column(Integer, primary_key=True)
    username = Column(String, index=True)
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