from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

# DATABASE CONNECTION
# Replace 'YOUR_PASSWORD' with your actual MySQL Workbench password
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/grievance_system'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- 1. USER TABLE (For Registration) ---
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

# --- 2. COMPLAINT TABLE (For Submissions) ---
class Complaint(db.Model):
    __tablename__ = 'complaints'
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Pending')

# Auto-create tables in Workbench
with app.app_context():
    db.create_all()

# --- ROUTES ---

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already exists"}), 400
    
    hashed_pw = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(fullname=data['fullname'], email=data['email'], password=hashed_pw)
    
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Registration Data Saved in DB"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        return jsonify({"name": user.fullname, "email": user.email}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/submit-complaint', methods=['POST'])
def submit_complaint():
    data = request.json
    new_complaint = Complaint(
        user_email=data['email'],
        category=data['category'],
        description=data['description']
    )
    db.session.add(new_complaint)
    db.session.commit()
    return jsonify({"message": "Complaint Data Saved in DB"}), 201
if __name__ == '__main__':
   app.run(debug=True, port=5000)