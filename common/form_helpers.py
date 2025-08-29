# -*- coding: utf-8 -*-
import io, logging
from typing import Callable, Tuple, Optional
from flask import Request, session
from . import utils

logger = logging.getLogger(__name__)

def is_retry(request: Request) -> bool:
    """POSTパラメータの is_retry を真偽値化"""
    return request.form.get('is_retry', '').lower() == 'true'


def load_csv_from_request(
    request: Request,
    read_csv_fn: Callable
) -> Tuple[bool, Optional[str], Optional[str], list[str]]:
    """
    アップロードされたCSVを読み取り、（bool、ファイル名、ジャンル、ことばリスト）を返す。
    成功時はセッションにも保存する。
    ファイル未指定等なら、bool:False
    """
    read_csv_fn_name = getattr(read_csv_fn, "__name__", str(read_csv_fn))
    logging.info('Call utils.load_csv_from_request() request=%s read_csv_fn=%s', request, read_csv_fn_name)
    file = request.files.get("csv_file")
    if not (file and file.filename):
        return False, None, None, []

    utf8_text = utils.csv_decode_utf8(file)             # bytes を str に変換
    genre, words = read_csv_fn(io.StringIO(utf8_text))  # str を StringIO に包んで渡す
    words = words or []
    filename = file.filename
    session['filename'] = filename
    session['genre'] = genre
    session['words'] = words
    return True, filename, genre, words


def load_genre_words(
    request: Request,
    read_csv_fn: Callable,
    use_session_when_retry: bool = True,
) -> Tuple[Optional[str], list[str], str]:

    """
    CSV or セッションから (genre, words) を取得。
    戻り値: (genre, words, source)  # source in {'csv','session','none'}
    """
    genre = None
    words = []
    source = 'none'

    # リトライモードの場合、セッション情報からジャンルと単語を取得
    if use_session_when_retry and request.form.get('is_retry', '').lower() == 'true':
        genre = session.get('genre')
        words = session.get('words') or []
        return genre, words, ('session' if (genre and words) else 'none')

    # CSVファイルを読み込んだ場合、CSVファイルからジャンルと単語を取得
    file = request.files.get('csv_file')
    if file and file.filename:
        genre, words = read_csv_fn(file.stream)
        words = words or []
        session['genre'] = genre
        session['words'] = words
        source = 'csv'
    return genre, words, source


def parse_int(
    request: Request,
    name: str,
    default: int,
    min_value: Optional[int] = None,
    max_value: Optional[int] = None
) -> Tuple[bool, int]:
    """フォーム値を int 化。失敗時は default。"""
    try:
        v = int(request.form.get(name, default))
    except (TypeError, ValueError):
        return True, default
    if (min_value is not None) and v < min_value:
        v = min_value
    if (max_value is not None) and v > max_value:
        v = max_value
    return False, v


def save_manual_from_request(request: Request) -> Tuple[str, list[str]]:
    """
    フォームからの手入力（ジャンル/ことば[]）を読み取り、空白除去してセッションに保存
    """
    logging.info('Call save_manual_from_request()')
    genre = (request.form.get('genre') or '').strip()
    words = [w.strip() for w in request.form.getlist('words')]
    words = [w for w in words if w]   # 空白除去
    session['genre'] = genre
    session['words'] = words
    logging.info('return save_manual_from_request() genre=%s words_count=%s', genre, len(words))
    return genre, words