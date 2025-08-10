from flask import Flask
from top import top_bp
from narabikae import narabikae_bp

app = Flask(__name__, template_folder='common/templates')
app.secret_key = 'Study-Print-Sheet_SubWork_Get_50000_Over'

# Blueprint登録
app.register_blueprint(top_bp)
app.register_blueprint(narabikae_bp)


if __name__ == '__main__':
    app.run(debug=True)
