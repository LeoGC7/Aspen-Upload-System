from flask import Flask, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from hashlib import sha256
import os

app = Flask(__name__)

app.secret_key = '123'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db' #Example using sqlite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppress deprecation warning

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    user_hash = db.Column(db.String(256), unique=True, nullable=False)

    def generate_user_hash(self):
        full_string = f'{self.username}{self.password}'.encode('utf-8')
        self.user_hash = sha256(full_string).hexdigest()
        return self.user_hash
    
    def generate_password_hash(self):
        self.password = sha256(self.password.encode('utf-8')).hexdigest()

    def verify_password(self, password):
        hashed_password = sha256(password.encode('utf-8')).hexdigest()
        return hashed_password == self.password

    def __repr__(self):
        return '<User %r>' % self.username

# Create the database tables
with app.app_context():
    db.create_all()

UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 * 1024

@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    
    if request.method == "POST":
        data = request.form

        username_ = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username = username_).first()

        if not user:
            return render_template('login.html', error = "The username or password is incorrect")

        if not user.verify_password(password):
            return render_template('login.html', error = "The username or password is incorrect")
        
        session['user_hash'] = user.user_hash

        return redirect(url_for('dashboard'))


@app.route('/register', methods = ["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')
    
    if request.method == "POST":
        data = request.form

        email_ = data.get('email')
        username_= data.get('username')
        password_ = data.get('password')

        new_user = User(email = email_, username = username_, password = password_)
        new_user.generate_user_hash()
        new_user.generate_password_hash()

        db.session.add(new_user)
        db.session.commit()

        print(data)
    
    return redirect(url_for('login'))

@app.route('/upload_video/<user_hash>', methods = ["GET", "POST"])
def upload(user_hash):
    if request.method == "GET":
        return render_template('index.html')

    if request.method == "POST":
        if 'video' not in request.files:
            return "No file uploaded", 400

        video = request.files['video']

        if video.filename == '':
            return "No file selected", 400

        video_path = os.path.join(app.config['UPLOAD_FOLDER'], user_hash)

        if not os.path.exists(video_path):
            os.makedirs(video_path)

        video_path = os.path.join(video_path, video.filename)

        video.save(video_path)


@app.route('/dashboard')
def dashboard():
    user_hash = session.get('user_hash')

    if not user_hash:
        return redirect(url_for('login'))

    user = User.query.filter_by(user_hash=user_hash).first()
    
    username = user.username 

    video_path = os.path.join(app.config['UPLOAD_FOLDER'], user_hash)

    if not os.path.exists(video_path):
        os.makedirs(video_path)

    videos = os.listdir(video_path)

    return render_template('dashboard.html', videos = videos, user_hash = user_hash, username = username)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)