from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# initialize database
db = SQLAlchemy(app)

# create model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False) # nullable = prevent blank
    email = db.Column(db.String(200), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Name %r>' % self.name

@app.get("/")
def index():
    return render_template('index.html')

@app.route("/user/<name>")
def user(name):
    user_data = {
        "name": name,
        "email": "john.doe@example.com"
    }

    extra = request.args.get("extra")
    if extra:
        user_data["extra"] = extra

    return jsonify(user_data), 200

@app.route("/create-user", methods=["POST"])
def create_user():
    if request.method == "POST":
        data = request.get_json()

        return jsonify(data), 201


if __name__ == "__main__":
    app.run(debug=True)