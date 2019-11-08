
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('api.config.BaseConfig')
jwt = JWTManager(app)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

from api.api import api
app.register_blueprint(api, url_prefix="/api")

from api.models import db
db.init_app(app)
migrate = Migrate(app, db)

if __name__ == '__main__':
  app.run()
