# -*- coding: utf-8 -*-
import random
import csv
from typing import List, Tuple

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

# CSVファイルからジャンル名と単語リストを取得
# 【使用アプリ】
# ことば並び替え
def read_csv(file_stream) -> Tuple[str, List[str]]:
    csv_text = file_stream.read().decode('utf-8').splitlines()
    reader = csv.reader(csv_text)

    rows = list(reader)
    genre = rows[0][0]  # 1行目（ジャンル名）
    words = [row[0] for row in rows[1:] if row]  # 2行目以降（単語リスト）

    return genre, words

# 単語リストからランダムに出題数分抽出
# 【使用アプリ】
# ことば並び替え
def select_questions(words: List[str], count: int) -> List[str]:
    return random.sample(words, min(count, len(words)))
