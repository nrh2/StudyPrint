# -*- coding: utf-8 -*-
import logging
from flask import render_template, request, session, redirect, url_for, flash
from common import form_helpers
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
        logger.info("%s：リクエスト受信（ポスト）", page_title)
        action = request.form.get('action')

        # 1) CSVファイルを選択 ⇒ セッション保存
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

        # 2）手入力 ⇒ セッション保存
        if action == 'manual_save':
            logging.info('%s：手入力ボタン押下', page_title)
            manual_genre, manual_words = form_helpers.save_manual_from_request(request)
            logger.info("%s：正常に手入力保存 ジャンル=%s 単語数=%d", page_title, manual_genre, len(manual_words))
            return redirect(url_for('narabikae.index'))

        # 3）問題を作成
        if action == 'generate':
            logging.info('%s：問題を作成ボタン押下', page_title)
            filename = session.get('filename')
            csv_genre = session.get('genre')
            csv_words = session.get('words', [])
            manual_genre = session.get('manual_genre')
            manual_words = session.get('manual_words', [])
            source_prefer = request.form.get('source_prefer', '').strip().lower()
            logging.info('%s：filename=%s csv_genre=%s len(csv_words)=%s manual_genre=%s len(manual_words)=%s source_prefer=%s',\
                         page_title, filename, csv_genre, len(csv_words), manual_genre, len(manual_words), source_prefer)

            # CSV・手入力 両方あり＆未選択 ⇒ 選択ダイアログ表示のためテンプレ再描画
            if (csv_genre and manual_genre) and (csv_words and manual_words) and source_prefer not in {'csv', 'manual'}:
                logger.info("%s：入力データが両方（CSVファイル、手入力）あり、選択待ち", page_title)
                flash('CSVと手入力の両方が存在します。どちらを使用するか選択してください。')
                return render_template(
                    'narabikae.html',
                    title=page_title,
                    kana_modes=KANA_MODES,
                    default_count=DEFAULT_QUESTION_COUNT,
                    session_filename=filename,
                    session_genre=csv_genre,
                    session_words=csv_words,
                    manual_genre=manual_genre,
                    manual_words=manual_words,
                    need_source_choice=True,
                    default_manual_count=DEFAULT_MANUAL_INPUT_COUNT
                )

            # 使用ソース決定
            if source_prefer == 'manual' or (manual_genre and manual_words and not csv_words):
                logging.info("%s：手入力データ使用", page_title)
                genre, words = manual_genre, manual_words
                used_source = 'manual'
            else:
                logging.info("%s：CSVデータ使用", page_title)
                genre, words = csv_genre, csv_words
                used_source = 'csv'

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
            logger.info("%s：かなモード設定=%s", page_title, kana_mode)

            # 出題単語抽出 & 単語シャッフル
            selected_words = select_questions(words, question_count)
            shuffled_words = [shuffle_word(w) for w in selected_words]
            logger.info("%s：問題生成完了 生成数=%d", page_title, len(shuffled_words))
            logger.info("%s：問題生成完了 生成数=%d", page_title, len(shuffled_words))

            # 問題文生成
            question_text = QUESTION_TEMPLATE.format(genre=genre)
            logger.info("%s：問題文生成完了", page_title)
            logger.info("%s：問題文生成完了", page_title)

            # 結果画面描画
            return render_template(
                'narabikae_print.html',
                title=page_title,
                question_text=question_text,
                words=shuffled_words,
                count=question_count,
                kana_mode=kana_mode,
                used_source=used_source,
                back_url=url_for(f"{sheet_key}.index")
            )

    # request.method == GET（画面表示）
    logger.info("%s：初期表示（GET）", page_title)
    logging.info('%s：filename=%s csv_genre=%s len(csv_words)=%s manual_genre=%s len(manual_words)=%s source_prefer=%s',
                 page_title,
                 session.get('filename'),
                 session.get('csv_genre'),
                 len(session.get('csv_words', [])),
                 session.get('manual_genre'),
                 len(session.get('manual_words', [])),
                 session.get('source_prefer')
    )
    return render_template(
        'narabikae.html',
        title=page_title,
        kana_modes=KANA_MODES,
        session_filename=session.get('filename'),
        session_genre=session.get('csv_genre'),
        session_words=session.get('csv_words'),
        manual_genre=session.get('manual_genre'),
        manual_words=session.get('manual_words'),
        default_count=DEFAULT_QUESTION_COUNT
    )