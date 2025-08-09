from flask import Flask
from top import top_bp

app = Flask(__name__)

# Blueprint登録
app.register_blueprint(top_bp)


if __name__ == '__main__':
    app.run(debug=True)
