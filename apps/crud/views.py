from apps.crud.forms import UserForm
# dbをimportする
from apps.app import db
# Userクラスをimportする
from apps.crud.models import User

from flask_login import login_required
from flask import Blueprint, render_template, redirect, url_for, Response

# Blueprintでcrudアプリを生成する
crud = Blueprint(
    "crud",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@crud.after_request
def add_header(response: Response):
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response



@crud.route("/sql")
@login_required
def sql():
    a = db.session.query(User).count()
    return f"コンソールログを確認してください{a}"

@crud.route("/users/new", methods=["GET", "POST"])
@login_required
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

@crud.route("/users")
@login_required
def users():
    # ユーザ一覧を取得する
    users = User.query.all()
    return render_template("crud/index.html", users=users)

@crud.route("/users/<user_id>", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    form: UserForm = UserForm()

    # Userモデルを利用してユーザーを取得する
    user: User = User.query.filter_by(id=user_id).first()

    # fromからサブミットされた場合はユーザを更新し、ユーザーの一覧画面へリダイレクトする
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("crud.users"))
    
    # GETの場合はHTMLを返す
    return render_template("crud/edit.html", user=user, form=form)


@crud.route("/users/<user_id>/delete", methods=["GET", "POST"])
@login_required
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("crud.users"))