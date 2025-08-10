# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for
from . import top_bp
from common.constants import APP_INFO, SHEET_INFO

sheet_key = top_bp.name
page_title = APP_INFO[sheet_key]["label"]

# トップページ処理
@top_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # シート名選択
        selected_sheet = request.form.get('sheet_name')

        # 存在しないシート名が選択された場合の処理
        if selected_sheet not in SHEET_INFO:
            return "不正なシート名が選択されました。", 400

        # Blueprint名+関数名でURL生成
        return redirect(url_for(f"{selected_sheet}.index"))

    # GETリクエスト時（初期表示）
    return render_template(
        'top.html',
        title=page_title,
        sheet_infos=SHEET_INFO
    )