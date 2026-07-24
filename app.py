# imports

from dotenv import load_dotenv
import os
from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    flash
)

from routes.admin_routes import admin_bp
from routes.student_routes import students_bp
from routes.teacher_routes import teachers_bp

from database import (
    initialise_database,
    setup_admin
)

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

initialise_database()
setup_admin()

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
    return render_template("exit.html")

@app.errorhandler(404)
def not_found(error):
    return render_template("errors/404.html"), 404

@app.errorhandler(403)
def forbidden(error):
    return render_template("errors/403.html"), 403

@app.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html"), 500

if __name__ == '__main__':
    app.run(debug=True)