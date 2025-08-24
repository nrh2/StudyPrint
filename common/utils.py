# -*- coding: utf-8 -*-
import io, chardet, logging, random
import csv
from typing import List, Tuple, Callable, Optional
from flask import Request, session

logger = logging.getLogger(__name__)

# 単語の文字順をランダムに並び替える（元と同じ順序は除外）
# 【使用アプリ】
# ことば並び替え
def shuffle_word(word: str) -> str:
    chars = list(word)
    while True:
        random.shuffle(chars)
        shuffled = ''.join(chars)
        if shuffled != word:  # 元と異なる順序になったら終了
            return shuffled


# 単語リストからランダムに出題数分抽出
# 【使用アプリ】
# ことば並び替え
def select_questions(words: List[str], count: int) -> List[str]:
    return random.sample(words, min(count, len(words)))


# =====================================================================================
# CSVファイル関係
# =====================================================================================

# CSVファイルがUTF-8で読み込めるか確認。読み込めない場合、utf-8にデコード。
#【使用アプリ】
# ことば並び替え
def csv_decode_utf8(file) -> str:
    logging.info('Call form_helpers.csv_decode_utf8() file.name="%s"', file.filename)
    raw = file.read()   # バイナリ読込

    # UTF-8で読めるか確認
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        result = chardet.detect(raw)
        encoding = result["encoding"] or "utf-8"
        text = raw.decode(encoding, errors="replace")
    return text


# CSVファイルからジャンル名と単語リストを返す
# 【使用アプリ】
# ことば並び替え
def read_csv(file_stream) -> Tuple[str, List[str]]:
    logging.info('Call utils.read_csv')
    csv_text = file_stream.read().splitlines()
    reader = csv.reader(csv_text)

    rows = list(reader)
    genre = rows[0][0]  # 1行目（ジャンル名）
    words = [row[0] for row in rows[1:] if row]  # 2行目以降（単語リスト）

    return genre, words