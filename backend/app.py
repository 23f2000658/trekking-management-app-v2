from flask import Flask, jsonify, request # type: ignore
from flask_cors import CORS # type: ignore
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt, get_jwt_identity # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash # type: ignore
from models import db, User, Trek, Booking
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trekking.db'
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
db.init_app(app)
CORS(app)
jwt = JWTManager(app)

def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorated_view(*args, **kwargs):
            claims = get_jwt()
            if claims.get("role") != role:
                return jsonify({"error": "Access denied"}), 403
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Trekking API!"}), 200

@app.route('/api/admin/create-staff', methods=['POST'])
def create_staff():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'])
    
    new_staff = User(
        username=data['name'],
        email=data['email'],
        password_hash=hashed_password,
        role='staff' 
    )
    
    db.session.add(new_staff)
    db.session.commit()
    
    return jsonify({"message": "Staff created successfully!"}), 201

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 409
    
    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        role='user' 
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User registered successfully!"}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    print(f"DEBUG: Received data: {data}")
    
    user = User.query.filter_by(username=data.get('username')).first()
    
    if not user:
        print("DEBUG: User not found in database!")
        return jsonify({"error": "Invalid credentials"}), 401

    is_valid = check_password_hash(user.password_hash, data.get('password'))
    print(f"DEBUG: Password check result: {is_valid}")
    
    if is_valid:
        access_token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
        return jsonify({"access_token": access_token, "role": user.role, "user_id": user.id})
        
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/api/auth/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({
        "id": user.id,
        "username": user.username,
        "role": user.role
    }), 200

@app.route('/api/admin/treks', methods=['POST'])
@role_required('admin')
def create_trek():
    data = request.get_json()
    new_trek = Trek(
        name=data['name'], 
        location=data['location'],
        available_slots=data['slots'],
        total_slots=data['slots'],
        start_date=datetime.fromisoformat(data['start_date'])
    )
    db.session.add(new_trek)
    db.session.commit()
    return jsonify({"message": "Trek created"}), 201

@app.route('/api/staff/update-trek/<int:trek_id>', methods=['PUT'])
@role_required('staff')
def update_trek_status(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    # Check if this staff is assigned to this trek
    if trek.staff_id != get_jwt_identity():
        return jsonify({"error": "Not authorized for this trek"}), 403
    
    trek.status = request.json.get('status')
    db.session.commit()
    return jsonify({"message": "Status updated"})

@app.route('/api/user/book', methods=['POST'])
@role_required('user')
def book_trek():
    data = request.get_json()
    trek = Trek.query.get(data['trek_id'])
    if trek.available_slots > 0:
        booking = Booking(user_id=get_jwt_identity(), trek_id=trek.id)
        trek.available_slots -= 1
        db.session.add(booking)
        db.session.commit()
        return jsonify({"message": "Booked successfully"})
    return jsonify({"error": "No slots available"}), 400

with app.app_context():
    db.create_all()  
    
    admin = User.query.filter_by(username='Naman').first()
    if not admin:
        admin = User(
            username='Naman',
            email='admin@trekking.com',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully!")
    else:
        print("Admin already exists, skipping creation.")


if __name__ == '__main__':
    app.run(debug=True)

