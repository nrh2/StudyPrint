# -*- coding: utf-8 -*-
import io
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
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
        # POSTパラメータ（文字列型）からブール型に変換
        is_retry = request.form.get('is_retry') == 'true'

        genre = None
        words = None

        if is_retry:
            # 問題再作成ボタン押下：セッションから復元
            genre = session.get('genre')
            words = session.get('words')

        else:
            # 初回モード（CSVファイル必須）
            file = request.files.get('csv_file')

            # CSVファイルが読み込まれていない場合、トップへ促す
            if file and file.filename:
                genre, words = read_csv(file.stream)
                session['genre'] = genre
                session['words'] = words

        if not genre or not words:
                flash('先にCSVファイルをアップロードしてください。')
                return redirect(url_for('narabikae.index'))

        # 出題数取得（未入力ならデフォルト値）
        try:
            count = int(request.form.get('count', DEFAULT_QUESTION_COUNT))
        except (TypeError, ValueError):
            count = DEFAULT_QUESTION_COUNT

        # カナモード取得（今は未使用、将来拡張用）
        kana_mode = request.form.get('kana_mode', 'hiragana')

        # 出題単語抽出 & 単語シャッフル
        selected_words = select_questions(words, count)
        shuffled_words = [shuffle_word(w) for w in selected_words]

        # 問題文生成
        question_text = QUESTION_TEMPLATE.format(genre=genre)

        # 結果画面描画
        return render_template(
            'narabikae_print.html',
            title=PAGE_TITLE_PRINT,
            question_text=question_text,
            words=shuffled_words,
            count=count,
            kana_mode=kana_mode
        )

    # GET（初期表示）
    return render_template(
        'narabikae.html',
        title=PAGE_TITLE,
        kana_modes=KANA_MODES,
        default_count=DEFAULT_QUESTION_COUNT
    )