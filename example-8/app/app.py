from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test.db'
app.config["SECRET_KEY"] = "very-secret-key"
db = SQLAlchemy(app)

Bootstrap(app)

from views import index, users, devices
import models

db.create_all()

if __name__ == "__main__":
    app.register_blueprint(index.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(devices.bp)
    app.run(host="0.0.0.0", port=5005, debug=True)