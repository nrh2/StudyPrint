import os, logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

from flask import Flask, request, g
from top import top_bp
from narabikae import narabikae_bp

def setup_logging(app: Flask):
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "app.log")

    # 重複追加を防止（デバッグ再起動・多重登録対策）
    if any(isinstance(h, TimedRotatingFileHandler) for h in app.logger.handlers):
        return

    handler = TimedRotatingFileHandler(
        filename=log_file,
        when="midnight",        # 毎日0時にローテーション
        interval=1,
        backupCount=30,          # 30日保存
        encoding="utf-8",
        utc=False,              # ローカルタイム
    )

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # handler設定
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)

    # appログ設定
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.propagate = False        # ルートロガーへ伝播させない（重複防止）

    root = logging.getLogger()
    if not any(isinstance(h, TimedRotatingFileHandler) for h in root.handlers):
        root.addHandler(handler)

    if root.level > logging.INFO:
        root.setLevel(logging.INFO)


def setup_access_log(app: Flask):
    @app.before_request
    def  _mark_start():
        g._req_start = datetime.now()

    @app.after_request
    def _log_access(resp):
        try:
            dur_ms = 0
            if hasattr(g, "_req_start"):
                dur_ms = int((datetime.now() - g._req_start).total_seconds() * 1000)

            app.logger.info(
                "access remote=%s method=%s path=%s status=%s ua=%s dur_ms=%s",
                request.headers.get("X-Forwarded-For", request.remote_addr),    # プロキシやロードバランサー経由の場合、実際のクライアントIPは X-Forwarded-For ヘッダに入ります
                                                                                # なければ request.remote_addr（直接接続してきたIP）を使う
                request.method,                                                 # HTTPメソッド（GET, POST, PUT, DELETE など）
                request.full_path if request.query_string else request.path,    # クエリ文字列付きのパス（/search?q=python など）を取得。クエリがない場合は単純なパス（/top）だけ
                resp.status_code,                                               # HTTPステータスコード（200, 404, 500 など）
                request.headers.get("User-Agent", "-"),                         # ブラウザやアプリの識別情報（例: Mozilla/5.0 ...）。なければ "-"。
                dur_ms,                                                         # 処理時間（ミリ秒単位）
            )

        except Exception:
            pass

        return resp

app = Flask(__name__, template_folder='common/templates')
app.secret_key = 'Study-Print-Sheet_SubWork_Get_50000_Over'

# ログ初期化
setup_logging(app)
setup_access_log(app)

# Blueprint登録
app.register_blueprint(top_bp)
app.register_blueprint(narabikae_bp)


if __name__ == '__main__':
    app.run(debug=True)
