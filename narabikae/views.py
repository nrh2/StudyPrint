# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request
from . import narabikae_bp
from common.constants import KANA_MODES
from .constants import (
    PAGE_TITLE, PAGE_TITLE_PRINT,
    QUESTION_TEMPLATE, DEFAULT_QUESTION_COUNT
)
from common.utils import shuffle_word, read_csv, select_questions

@narabikae_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # CSVファイル取得
        file = request.files['csv_file']
        # 出題数取得（未入力ならデフォルト値）
        count = int(request.form.get('count', DEFAULT_QUESTION_COUNT))
        # カナモード取得（今は未使用、将来拡張用）
        kana_mode = request.form.get('kana_mode', 'hiragana')

        # CSV読み込み
        genre, words = read_csv(file.stream)

        # 出題単語抽出
        selected_words = select_questions(words, count)

        # 単語をシャッフル
        shuffled_words = [shuffle_word(w) for w in selected_words]

        # 問題文生成
        question_text = QUESTION_TEMPLATE.format(genre=genre)

        # 結果画面描画
        return render_template(
            'narabikae_print.html',
            title=PAGE_TITLE_PRINT,
            question_text=question_text,
            words=shuffled_words
        )

    # GETリクエスト時（初期表示）
    return render_template(
        'narabikae.html',
        title=PAGE_TITLE,
        kana_modes=KANA_MODES,
        default_count=DEFAULT_QUESTION_COUNT
    )