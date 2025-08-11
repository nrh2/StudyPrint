# -*- coding: utf-8 -*-
import logging
from flask import render_template, request, redirect, url_for
from . import top_bp
from common.constants import APP_INFO, SHEET_INFO

logger = logging.getLogger(__name__)

sheet_key = top_bp.name
page_title = APP_INFO[sheet_key]["label"]

# トップページ処理
@top_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # シート名選択
        selected_sheet = request.form.get('sheet_name')
        logger.info("トップ：シート選択を受信 選択シート名=%s", selected_sheet)

        # 存在しないシート名が選択された場合の処理
        if selected_sheet not in SHEET_INFO:
            logger.warning("%s：不正なシート名が選択されました 選択シート名：%s", page_title, selected_sheet)
            return "不正なシート名が選択されました。", 400

        dest_endpoint = f"{selected_sheet}.index"
        logger.info("トップ：画面遷移を実施 遷移先=%s", dest_endpoint)
        # Blueprint名+関数名でURL生成
        return redirect(url_for(dest_endpoint))

    # GETリクエスト時（初期表示）
    logger.info("トップ：画面表示 シート数=%d", len(SHEET_INFO))
    return render_template(
        'top.html',
        title=page_title,
        sheet_infos=SHEET_INFO
    )