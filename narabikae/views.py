# -*- coding: utf-8 -*-
import logging
from flask import flash, redirect, render_template, request, Response, session, url_for
from urllib.parse import quote
from common import form_helpers, utils
from common.constants import KANA_MODES, SHEET_INFO
from common.utils import shuffle_word, read_csv, select_questions
from . import narabikae_bp
from .constants import (
    QUESTION_TEMPLATE,
    DEFAULT_QUESTION_COUNT,
    DEFAULT_MANUAL_INPUT_COUNT,
)

logger = logging.getLogger(__name__)

sheet_key = narabikae_bp.name
page_title = SHEET_INFO[sheet_key]["label"]

@narabikae_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')
        logger.info("%s：リクエスト受信（ポスト） action=%s", page_title, action)

        # CSVファイルを選択 ⇒ セッション保存
        if action == 'csv_load':
            logging.info('%s：CSV読込', page_title)
            csv_load_success, filename, genre, words = form_helpers.load_csv_from_request(request, read_csv)

            if csv_load_success:
                logger.info("%s：正常にCSVファイル読込 ファイル名=%s ジャンル=%s 単語数=%d", page_title, filename, genre, len(words))
                session['filename'] = filename
                session['genre'] = genre
                session['words'] = words
            else:
                logger.warning("%s：CSVファイルが未指定です。", page_title)
            return redirect(url_for('narabikae.index'))

        # セッション情報を削除
        if action == 'csv_reset':
            logging.info('%s：セッション情報削除', page_title)
            session['filename'] = None
            session['genre'] = ""
            session['words'] = []
            logging.info('%s：セッション情報削除完了 filename=%s, genre=%s, words_count=%s', page_title, session['filename'], session['genre'], len(session['words']))



        # 手入力ボタン ⇒ 保存ボタン
        if action == 'manual_save':
            # フォームからジャンルとことばリストを取得
            genre, words = form_helpers.save_manual_from_request(request)
            logging.info('genre=%s words_count=%s', genre, len(words))
            try:
                # 取得したジャンルとことばを使用し、CSV文字列を作成
                csv_text = utils.create_csv_text(genre, words)

                logging.info('%s：CSVファイル作成 genre=%s words_count=%s', page_title, session['genre'], len(session['words']))

                filename = session['filename']
                quoted_filename = quote(filename)

                # レスポンスを返す（ユーザーが保存先を選択）
                return Response(
                    csv_text,
                    mimetype="text/csv; charset=utf-8",
                    headers={
                        "Content-Disposition": f"attachment; filename*=UTF-8''{quoted_filename}"
                    }
                )

            except Exception as e:
                logging.error("%s：CSVファイル作成失敗 error=%s", page_title, str(e))
                flash("CSVファイルの作成に失敗しました。")
                return redirect(url_for('narabikae.index'))


        # 問題を作成
        if action == 'generate':
            logging.info('%s：問題を作成ボタン押下', page_title)
            filename = session.get('filename')
            genre = session.get('genre')
            words = session.get('words', [])
            source_prefer = request.form.get('source_prefer', '').strip().lower()
            logging.info('%s：filename=%s genre=%s len(words)=%s source_prefer=%s',\
                        page_title, filename, genre, len(words), source_prefer)

            if not genre or not words:
                logging.warning("%s：ジャンルもしくは単語の有効なデータがありません。", page_title)
                flash('ジャンル、もしくは単語に有効なデータがありません。')
                return redirect(url_for('narabikae.index'))

            # 出題数を取得（不正の場合、デフォルト値に矯正）
            is_invalid, question_count = form_helpers.parse_int(
                request, 'question_count', DEFAULT_QUESTION_COUNT, min_value = 1
            )
            if is_invalid:
                logging.info("%s：正常に出題数を取得 出題数=%s", page_title, question_count)
            else:
                logging.warning("%s：出題数が不正のため、デフォルト値に矯正 デフォルト値=%s",
                                page_title, DEFAULT_QUESTION_COUNT)

            # カナモード取得（今は未使用、将来拡張用）
            kana_mode = request.form.get('kana_mode', 'hiragana')
            logger.info("%s：かなモード設定=%s", page_title, kana_mode)

            # 出題単語抽出 & 単語シャッフル
            selected_words = select_questions(words, question_count)
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
                count=question_count,
                kana_mode=kana_mode,
                back_url=url_for(f"{sheet_key}.index")
            )

    # request.method == GET（画面表示）
    logger.info("%s：初期表示（GET）", page_title)
    logging.info('%s：filename=%s genre=%s len(words)=%s',
                page_title,
                session.get('filename'),
                session.get('genre'),
                len(session.get('words', []))
    )
    return render_template(
        'narabikae.html',
        title=page_title,
        kana_modes=KANA_MODES,
        filename=session.get('filename'),
        genre=session.get('genre'),
        words=session.get('words'),
        default_count=DEFAULT_QUESTION_COUNT,
        default_manual_input_count=DEFAULT_MANUAL_INPUT_COUNT
    )