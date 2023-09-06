from flask import Flask
from views.main import main_bp
from views.api import api_bp


app = Flask(__name__)

app.register_blueprint(main_bp)
app.register_blueprint(api_bp, url_prefix='/api')
app.secret_key = 'd3e3e12d36866b1a4a8661f41430b3520acc781f47479f7410a3ab298a85e9b094b38e865043c28ddabf919d6b5dd0369357'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
