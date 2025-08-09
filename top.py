# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, url_for
from constants import (
    PAGE_TITLE_TOP,SHEET_NAMES
)

top_bp = Blueprint('top', __name__)

# トップページ処理
@top_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # シート名選択
        selected_sheet = request.form.get('sheet_name')

        # 存在しないシート名が選択された場合の処理
        if selected_sheet not in SHEET_NAMES:
            return "不正なシート名が選択されました。", 400

        # Blueprint名+関数名でURL生成
        return redirect(url_for(f"{selected_sheet}.index"))

    # GETリクエスト時（初期表示）
    return render_template(
        'top.html',
        title=PAGE_TITLE_TOP,
        sheet_names=SHEET_NAMES
    )