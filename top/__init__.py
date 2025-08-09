# -*- coding: utf-8 -*-
from flask import Blueprint

# Blueprint を生成（この名前 'top' が url_for で使う Blueprint 名になります）
# template_folder はこの Blueprint 配下のテンプレート置き場
top_bp = Blueprint('top', __name__, template_folder='templates')

# ルート定義を読み込んで Blueprint に紐づける
from . import views  # noqa: E402,F401

