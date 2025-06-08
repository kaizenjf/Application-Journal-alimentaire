from flask import Flask, render_template, request, redirect, url_for,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User,Meal
from extensions import db  # <-- ici
import os
from werkzeug.utils import secure_filename
 

app = Flask(__name__)
app.secret_key = 'une_cle_secrete'  # utilisée pour sécuriser les sessions
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:jean973@localhost/journal_test'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db.init_app(app)  # <-- très important
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # redirige si l'utilisateur non connecté tente d'accéder à une page protégée


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("dashboard"))
        return "Email ou mot de passe incorrect"
    return render_template("auth.html")

@app.route("/register", methods=["POST"])
def register():
    pseudo = request.form['pseudo']
    email = request.form['email']
    password = request.form['password']
    hashed_pw = generate_password_hash(password)
    new_user = User(pseudo=pseudo, email=email, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("login"))


@app.route("/add_meal", methods=["GET", "POST"])
@login_required
def add_meal():
    if request.method == "POST":
        name = request.form['name']
        poids = float(request.form['poids'])
        quantite = int(request.form['quantite'])

        image = request.files['image']
        filename = None

        if image and image.filename != "":
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            image_url = f"/uploads/{filename}"
        else:
            image_url = None

        new_meal = Meal(
            name=name,
            poids=poids,
            quantite=quantite,
            image_url=image_url,
            user_id=current_user.id
        )
        db.session.add(new_meal)
        db.session.commit()
        return redirect(url_for("dashboard"))
    
    return render_template("add_meal.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)

