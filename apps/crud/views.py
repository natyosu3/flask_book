from apps.crud.forms import UserForm
# dbをimportする
from apps.app import db
# Userクラスをimportする
from apps.crud.models import User

from flask import Blueprint, render_template, redirect, url_for

# Blueprintでcrudアプリを生成する
crud = Blueprint(
    "crud",
    __name__,
    template_folder="templates",
    static_folder="static",
)

# indexエンドポイントを作成しindex.htmlを返す
@crud.route("/")
def index():
    return render_template("crud/index.html")

@crud.route("/sql")
def sql():
    a = db.session.query(User).count()
    return f"コンソールログを確認してください{a}"

@crud.route("/users/new", methods=["GET", "POST"])
def create_user():
    # UserFormをインスタンス化する
    form: UserForm = UserForm()
    # フォームの値をバリデートする
    if form.validate_on_submit():
        # ユーザを作成する
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        # ユーザを追加してコミットする
        db.session.add(user)
        db.session.commit()
        # ユーザの一覧画面へリダイレクトする
        return redirect(url_for("crud.users"))
    return render_template("crud/create.html", form=form)