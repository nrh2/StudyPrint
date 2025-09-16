# -*- coding: utf-8 -*-

# アプリ名
# えんぴつひまわり

# アプリ情報
APP_INFO = {
    "top" : {
        "label" : "知育プリントメーカー",
        "summary" : "文字書き練習",
        "endpoint" : "top.index",
        "icon" : ""
    }
}

# シート情報
SHEET_INFO = {
    "narabikae" : {
        "label" : "ならびかえて できる ことばは？",
        "summary" : "文字を並び変えて正しいことばを作る練習",
        "endpoint" : "narabikae.index",
        "icon" : "",
        "is_completed": True
    },
    "kotobasagasi": {
        "label" : "かくされた ことばを さがそう！",
        "summary" : "隠れた言葉を探す",
        "endpoint" : "kotobasagasi.index",
        "icon" : "",
        "is_completed": False
    },
    "zukeisagasi": {
        "label" : "かくされた ずけいを さがそう！",
        "summary" : "図形探し",
        "endpoint" : "zukeisagasi.index",
        "icon" : "",
        "is_completed": False
    },
    "keisann": {
        "label" : "けいさん できるかな？",
        "summary" : "四則演算の練習",
        "endpoint" : "keisann.index",
        "icon" : "",
        "is_completed": False
    }
}

# カナモード選択肢
KANA_MODES = {
    "hiragana": "ひらがな",
    "katakana": "カタカナ"
}
