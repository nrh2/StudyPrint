# -*- coding: utf-8 -*-
import logging
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from . import narabikae_bp
from common.constants import KANA_MODES, SHEET_INFO
from .constants import QUESTION_TEMPLATE, DEFAULT_QUESTION_COUNT
from common.utils import shuffle_word, read_csv, select_questions

logger = logging.getLogger(__name__)

sheet_key = narabikae_bp.name
page_title = SHEET_INFO[sheet_key]["label"]

@narabikae_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        logger.info("%s：リクエスト受信（ポスト）", page_title)

        # POSTパラメータ（文字列型）からブール型に変換
        is_retry = request.form.get('is_retry') == 'true'

        genre = None
        words = None

        if is_retry:
            # 問題再作成ボタン押下：セッションから復元
            genre = session.get('genre')
            words = session.get('words')
            logger.info("%s：CSVデータをセッションから復元 ジャンル=%s 単語数=%d", page_title, genre, len(words) if words else 0)

        else:
            # 初回モード（CSVファイル必須）
            file = request.files.get('csv_file')

            # CSVファイルが読み込まれていない場合、トップへ促す
            if file and file.filename:
                genre, words = read_csv(file.stream)
                session['genre'] = genre
                session['words'] = words
                logger.info("%s：CSVファイル読込 ファイル名=%s ジャンル=%s 単語数=%d", page_title, file.filename, genre, len(words))
            else:
                logger.warning("%s：CSVファイルが未指定です。", page_title)

        if not genre or not words:
            logger.warning("%s：CSVファイル入力不足（ジャンルもしくは単語なし）", page_title)
            flash('先にCSVファイルをアップロードしてください。')
            return redirect(url_for('narabikae.index'))

        # 出題数取得（未入力ならデフォルト値）
        try:
            count = int(request.form.get('count', DEFAULT_QUESTION_COUNT))
        except (TypeError, ValueError):
            count = DEFAULT_QUESTION_COUNT
            logger.warning("%s：出題数が不正のため、デフォルト値を使用 デフォルト値=%s", page_title, DEFAULT_QUESTION_COUNT)
        logger.info("%s：問題数=%d", page_title, count)

        # カナモード取得（今は未使用、将来拡張用）
        kana_mode = request.form.get('kana_mode', 'hiragana')
        logger.info("%s：かなモード設定=%s", page_title, kana_mode)

        # 出題単語抽出 & 単語シャッフル
        selected_words = select_questions(words, count)
        shuffled_words = [shuffle_word(w) for w in selected_words]
        logger.info("%s：問題生成完了 生成数=%d", page_title, len(shuffled_words))

        # 問題文生成
        question_text = QUESTION_TEMPLATE.format(genre=genre)
        logger.info("%s：問題文生成完了", page_title)

        # 結果画面描画
        return render_template(
            'narabikae_print.html',
            title=page_title,
            question_text=question_text,
            words=shuffled_words,
            count=count,
            kana_mode=kana_mode
        )

    # GET（初期表示）
    logger.info("%s：初期表示（GET）", page_title)
    return render_template(
        'narabikae.html',
        title=page_title,
        kana_modes=KANA_MODES,
        default_count=DEFAULT_QUESTION_COUNT
    )