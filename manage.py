from flask import Flask
from API import api
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
app.config['SWAGGER_UI_JSONEDITOR'] = True
api.init_app(app)
if __name__ == '__main__':
    app.run(debug=True)


