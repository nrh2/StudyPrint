# -*- coding: utf-8 -*-
from typing import Callable, Tuple, Optional
from flask import Request, session


def is_retry(request: Request) -> bool:
    """POSTパラメータの is_retry を真偽値化"""
    return request.form.get('is_retry', '').lower() == 'true'

def load_genre_words(
    request: Request,
    read_csv_fn: Callable,
    csv_field: str = 'csv_file',
    session_genre_key: str = 'genre',
    session_words_key: str = 'words',
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
        genre = session.get(session_genre_key)
        words = session.get(session_words_key) or []
        return genre, words, ('session' if (genre and words) else 'none')

    # CSVファイルを読み込んだ場合、CSVファイルからジャンルと単語を取得
    file = request.files.get(csv_field)
    if file and file.filename:
        genre, words = read_csv_fn(file.stream)
        words = words or []
        session[session_genre_key] = genre
        session[session_words_key] = words
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


def load_csv_from_request(
    request: Request,
    read_csv_fn: Callable,
    csv_field: str = 'csv_file',
    session_filename: str = 'filename',
    session_genre_key: str = 'genre',
    session_words_key: str = 'words'
) -> Tuple[bool, Optional[str], Optional[str], list[str]]:
    """
    アップロードされたCSVを読み取り、（bool、ファイル名、ジャンル、ワード）を返す。
    成功時はセッションにも保存する。
    ファイル未指定等なら、bool:False
    """
    file = request.files.get(csv_field)
    if not (file and file.filename):
        return False, None, None, []
    genre, words = read_csv_fn(file.stream)
    words = words or []
    session[session_filename] = file.filename
    session[session_genre_key] = genre
    session[session_words_key] = words
    return True, file.filename, genre, words


def save_manual_from_request(
    request: Request,
    session_genre_key: str = 'manual_genre',
    session_words_key: str = 'manual_words'
) -> Tuple[str, list[str]]:
    """フォームからの手入力（ジャンル/ことば[]）を読み取り、空白除去してセッションに保存"""
    manual_genre = (request.form.get('manual_genre') or '').strip()
    manual_words = [w.strip() for w in request.form.getlist('manual_words')]
    manual_words = [w for w in manual_words if w]   # 空白除去
    session[session_genre_key] = manual_genre
    session[session_words_key] = manual_words
    return manual_genre, manual_words


