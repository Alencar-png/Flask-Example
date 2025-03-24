from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from routers.security import auth_bp
from routers.users import users_bp
from routers.docs import docs_bp

app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)
app.register_blueprint(docs_bp)

if __name__ == "__main__":
    app.run(debug=True)
