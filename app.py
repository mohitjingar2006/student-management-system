# imports

from dotenv import load_dotenv
import os
from flask import (
    Flask,
    render_template
)

from routes.admin_routes import admin_bp
from routes.student_routes import students_bp
from routes.teacher_routes import teachers_bp

from database import initialise_database

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

initialise_database()

# register blueprints

app.register_blueprint(admin_bp)
app.register_blueprint(students_bp)
app.register_blueprint(teachers_bp)


# routes

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/exit")
def exit():
    return render_template(
        "home.html",
        message="Exiting..."
        )

if __name__ == '__main__':
    app.run(debug=True)