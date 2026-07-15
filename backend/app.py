from flask import Flask, jsonify, request 
from flask_cors import CORS 
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt, get_jwt_identity 
from werkzeug.security import generate_password_hash, check_password_hash 
from models import db, User, Trek, Booking
from datetime import datetime, timedelta
from functools import wraps
import csv
import io
from flask import make_response 
from tasks import export_csv
from tasks import send_trek_reminder
from tasks import generate_monthly_report
from celery.schedules import crontab 
from flask_mail import Mail 
from flask_caching import Cache 



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trekking.db'
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=8)
db.init_app(app)
CORS(app)
jwt = JWTManager(app)


app.config["CACHE_TYPE"] = "RedisCache"
app.config["CACHE_REDIS_URL"] = "redis://localhost:6379/1"

cache = Cache(app)

@app.route("/test-report")
def test_report():
    result = generate_monthly_report.delay()
    return f"Report Task Sent : {result.id}"

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

@app.route("/test-reminder")
def test_reminder():

    from tasks import send_trek_reminder

    result = send_trek_reminder.delay()

    return f"Reminder Task Sent : {result.id}"

@app.route("/test-export")
def test_export():

    from tasks import export_csv

    print(export_csv)
    print(type(export_csv))

    result = export_csv.delay(2)

    return f"Task Sent : {result.id}"


@app.route('/api/admin/create-staff', methods=['POST'])
def create_staff():
    data = request.get_json()
    
    
    new_staff = User(
        user_id=data['user_id'],
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
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
        user_id=data['user_id'],
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        role='user' 
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User registered successfully!"}), 201

@app.route('/api/admin/create-trek', methods=['POST'])
def create_trek_manual():
    data = request.get_json()
    
    new_trek = Trek(
        trek_id=data['trek_id'],
        name=data['name'],
        location=data['location'],
        difficulty=data['difficulty'],
        duration=int(data['duration']),
        total_slots=int(data['total_slots']),
        available_slots=int(data['total_slots']), 
        start_date=datetime.fromisoformat(data['start_date']),
        end_date=datetime.fromisoformat(data['end_date']),
        staff_id=data['staff_id'] 
    )
    
    db.session.add(new_trek)
    db.session.commit()

    cache.clear()
    
    return jsonify({"message": "Trek created successfully!"}), 201

@app.route('/api/treks', methods=['GET'])
@cache.cached(timeout=120)
def get_treks():
    
    all_treks = Trek.query.all()
    
    
    output = []
    for t in all_treks:
        trek_data = {
            "id": t.id,
            "name": t.name,
            "location": t.location,
            "difficulty": t.difficulty,
            "duration": t.duration,
            "total_slots": t.total_slots,
            "available_slots": t.available_slots
        }
        output.append(trek_data)
        
    return jsonify(output), 200

@app.route('/api/staff', methods=['GET'])
def get_Staff():

    all_staff = User.query.filter_by(role='staff').all()

    output = []

    for staff in all_staff:

        trek = Trek.query.filter_by(
            staff_id=staff.user_id
        ).first()

        output.append({

            "id": staff.id,
            "user_id": staff.user_id,
            "name": staff.username,
            "email": staff.email,
            "is_active": staff.is_active,
            "created_at": staff.created_at,

            "assigned": trek is not None,

            "trek_name": trek.name if trek else ""

        })

    return jsonify(output)

@app.route('/api/users', methods=['GET'])
def get_users():
    
    all_users = User.query.filter_by(role='user').all()
    
    output = []
    for u in all_users:
        user_data = {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "is_active": u.is_active,
            "created_at": u.created_at
        }
        output.append(user_data)
        
    return jsonify(output), 200


@app.route('/api/admin/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully!"}), 200

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    print(f"DEBUG: Received data: {data}")
    
    user = User.query.filter_by(username=data.get('username')).first()
    access_token = create_access_token(identity=user.id)
    if not user:
        print("DEBUG: User not found in database!")
        return jsonify({"error": "Invalid credentials"}), 401

    is_valid = check_password_hash(user.password_hash, data.get('password'))
    print(f"DEBUG: Password check result: {is_valid}")
    
    if is_valid:
        access_token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
        return jsonify({"access_token": access_token, "role": user.role, "user_id": user.id})
        
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/api/admin/trek/<int:trek_id>', methods=['DELETE'])
def delete_trek(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    db.session.delete(trek)
    db.session.commit()
    cache.clear()
    return jsonify({"message": "Trek deleted successfully!"}), 200

@app.route('/api/admin/staff/<int:staff_id>', methods=['DELETE'])
def delete_Staff(staff_id):
    Staff = User.query.get_or_404(staff_id)
    db.session.delete(Staff)
    db.session.commit()
    return jsonify({"message": "Staff deleted successfully!"}), 200

@app.route('/api/admin/assign-trek', methods=['POST'])
def assign_trek():
    data = request.get_json()
    staff_id = data.get('staff_id')
    trek_id = data.get('trek_id')
    
    print(f"DEBUG: Received staff_id={staff_id}, trek_id={trek_id}")

    trek = Trek.query.get(trek_id)
    if trek:
        trek.staff_id = staff_id 
        db.session.commit()
        return jsonify({"message": "Trek assigned to staff!"}), 200
    return jsonify({"error": "Trek not found"}), 404

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
    
    if trek.staff_id != get_jwt_identity():
        return jsonify({"error": "Not authorized for this trek"}), 403
    
    trek.status = request.json.get('status')
    db.session.commit()

    cache.clear()

    return jsonify({"message": "Status updated"})

@app.route('/api/staff/my-treks', methods=['GET'])
@role_required('staff')
def get_my_treks():

    current_id = get_jwt_identity()

    staff = User.query.get(int(current_id))

    treks = Trek.query.filter_by(
        staff_id=staff.user_id
    ).all()
    print("Matched Treks:", len(treks))

    output = []

    for t in treks:
        output.append({
            "id": t.id,
            "name": t.name,
            "location": t.location,
            "start_date": t.start_date.strftime("%d-%m-%Y"),
            "end_date": t.end_date.strftime("%d-%m-%Y"),
            "participants": len(t.bookings),
            "status": t.status
        })

    return jsonify(output), 200

@app.route('/api/staff/trek/<int:trek_id>', methods=['GET'])
@role_required('staff')
def get_trek_details(trek_id):

    current_id = get_jwt_identity()

    staff = User.query.get(int(current_id))

    trek = Trek.query.filter_by(
        id=trek_id,
        staff_id=staff.user_id
    ).first()

    if not trek:
        return jsonify({"error": "Trek not found"}), 404

    return jsonify({
        "id": trek.id,
        "name": trek.name,
        "available_slots": trek.available_slots,
        "status": trek.status
    }), 200

@app.route('/api/staff/trek/<int:trek_id>', methods=['PUT'])
@role_required('staff')
def update_trek(trek_id):

    current_id = get_jwt_identity()

    staff = User.query.get(int(current_id))

    trek = Trek.query.filter_by(
        id=trek_id,
        staff_id=staff.user_id
    ).first()

    if not trek:
        return jsonify({"error": "Trek not found"}), 404

    data = request.get_json()

    trek.available_slots = data["available_slots"]
    trek.status = data["status"]

    if data["status"] == "Completed":
        for booking in trek.bookings:
            booking.status = "Completed"

    db.session.commit()

    return jsonify({"message": "Trek updated successfully"}), 200

@app.route('/api/staff/trek/<int:trek_id>/participants', methods=['GET'])
@role_required('staff')
def get_participants(trek_id):

    current_id = get_jwt_identity()

    staff = User.query.get(int(current_id))

    trek = Trek.query.filter_by(
        id=trek_id,
        staff_id=staff.user_id
    ).first()

    if not trek:
        return jsonify({"error": "Trek not found"}), 404

    output = []

    for booking in trek.bookings:

        output.append({
            "booking_id": booking.id,
            "id": booking.user.id,
            "user_id": booking.user.user_id,
            "username": booking.user.username,
            "email": booking.user.email,
            "booking_date": booking.booking_date.strftime("%d-%m-%Y"),
            "status": booking.status
        })

    return jsonify(output), 200

@app.route('/api/staff/booking/<int:booking_id>', methods=['PUT'])
@role_required('staff')
def update_booking_status(booking_id):

    current_id = get_jwt_identity()

    staff = User.query.get(int(current_id))

    booking = Booking.query.get_or_404(booking_id)

    trek = Trek.query.get(booking.trek_id)

    if trek.staff_id != staff.user_id:
        return jsonify({"error": "Not Authorized"}), 403

    data = request.get_json()

    booking.status = data["status"]

    db.session.commit()

    return jsonify({
        "message": "Booking Updated"
    }), 200

@app.route('/api/staff/participants', methods=['GET'])
@role_required('staff')
def get_all_participants():

    current_id = get_jwt_identity()

    staff = User.query.get(int(current_id))

    treks = Trek.query.filter_by(staff_id=staff.user_id).all()

    output = []

    for trek in treks:

        for booking in trek.bookings:

            output.append({

                "booking_id": booking.id,
                "trek_name": trek.name,
                "user_id": booking.user.user_id,
                "username": booking.user.username,
                "email": booking.user.email,
                "booking_date": booking.booking_date.strftime("%d-%m-%Y"),
                "status": booking.status

            })

    return jsonify(output), 200


@app.route('/api/staff/<staff_id>', methods=['GET'])
def get_staff_profile(staff_id):
    staff = User.query.filter_by(id=staff_id).first()
    if staff:
        return jsonify({
            "id": staff.id,
            "name": staff.name,
            "email": staff.email,
            "contact": staff.contact,
            "status": staff.status,
            "bio": staff.bio 
        })
    return jsonify({"message": "Staff not found"}), 404

@app.route('/api/admin/stats', methods=['GET'])
@cache.cached(timeout=120)
def get_admin_stats():
    
    total_treks = Trek.query.count()
    users_count = User.query.filter_by(role='user').count()
    staff_count = User.query.filter_by(role='staff').count()
    total_bookings = Booking.query.count()

    
    print(f"DEBUG: Users={users_count}, Staff={staff_count}")
    
    stats = {
        "total_treks": total_treks,
        "total_users": users_count,
        "total_staff": staff_count,
        "total_bookings": total_bookings
    }
    return jsonify(stats)


@app.route('/api/admin/search-user', methods=['GET'])
@jwt_required()
def search_user():
    query = request.args.get('query')
    user = User.query.filter_by(user_id=query).first()
    if user:
        return jsonify({"type": "user", "data": {"name": user.username, "email": user.email}}), 200
    return jsonify({"message": "User not found"}), 404


@app.route('/api/admin/search-trek', methods=['GET'])
@jwt_required()
def search_trek():
    query = request.args.get('query')
    trek = Trek.query.filter_by(trek_id=query).first()
    if trek:
        return jsonify({"type": "trek", "data": {"name": trek.name, "location": trek.location, "difficulty": trek.difficulty}}), 200
    return jsonify({"message": "Trek not found"}), 404


@app.route('/api/bookings', methods=['GET'])
@role_required('admin')
def get_all_bookings():
    bookings = Booking.query.all()
    
    output = []
    for b in bookings:
        output.append({
            "id": b.id,
            "user_id": b.user.user_id,
            "user_name": b.user.username, 
            "trek_name": b.trek.name, 
            "location": b.trek.location,
            "date": b.booking_date.strftime('%Y-%m-%d'),
            "status": b.status
        })
    return jsonify(output)


@app.route('/api/trek-reports', methods=['GET'])
def get_trek_reports():
    treks = Trek.query.all()
    history = []
    total_conducted = len(treks)
    
    
    for t in treks:
        history.append({
            "name": t.name,
            "location": t.location,
            "participant_count": len(t.bookings) 
        })
    
    
    stats = {
        "total_treks": total_conducted,
        "top_trek": max(treks, key=lambda t: len(t.bookings)).name if treks else "N/A"
    }
    
    return jsonify({"history": history, "stats": stats})

@app.route("/api/user/history", methods=["GET"])
@role_required("user")
def trekking_history():

    user_id = get_jwt_identity()

    bookings = Booking.query.filter_by(user_id=user_id, status="Completed").all()

    history = []

    for booking in bookings:

        trek = Trek.query.get(booking.trek_id)

        history.append({
            "trek_name": trek.name,
            "booking_date": booking.booking_date,
            "status": booking.status
        })

    return jsonify(history), 200

@app.route('/api/user/treks', methods=['GET'])
@role_required('user')
@cache.cached(timeout=60)
def get_available_treks():

    current_user = int(get_jwt_identity())

    treks = Trek.query.filter_by(status="Open").all()

    output = []

    for t in treks:

        booking = Booking.query.filter_by(
            user_id=current_user,
            trek_id=t.id
        ).first()

        output.append({
            "id": t.id,
            "name": t.name,
            "location": t.location,
            "difficulty": t.difficulty,
            "duration": t.duration,
            "available_slots": t.available_slots,
            "status": t.status,
            "already_booked": booking is not None
        })

    return jsonify(output), 200

@app.route('/api/user/book', methods=['POST'])
@role_required('user')
def book_trek():

    data = request.get_json()

    user_id = int(get_jwt_identity())

    trek = Trek.query.get_or_404(data['trek_id'])


    existing_booking = Booking.query.filter_by(
        user_id=user_id,
        trek_id=trek.id
    ).first()

    if existing_booking:
        return jsonify({
            "error": "You have already booked this trek."
        }), 400

    
    if trek.available_slots <= 0:
        return jsonify({
            "error": "No slots available."
        }), 400

    booking = Booking(
        user_id=user_id,
        trek_id=trek.id,
        status="Booked"
    )

    trek.available_slots -= 1

    db.session.add(booking)
    db.session.commit()

    cache.clear()

    return jsonify({
        "message": "Trek booked successfully."
    }), 201

@app.route("/api/user/bookings", methods=["GET"])
@role_required("user")
def my_bookings():

    user_id = get_jwt_identity()

    bookings = Booking.query.filter_by(user_id=user_id, status="Booked").all()

    data = []

    for booking in bookings:

        trek = Trek.query.get(booking.trek_id)

        data.append({
            "booking_id": booking.id,
            "trek_name": trek.name,
            "location": trek.location,
            "duration": trek.duration,
            "booking_date": booking.booking_date,
            "status": booking.status
        })

    return jsonify(data), 200

@app.route("/api/user/export-csv", methods=["GET"])
@role_required("user")
def export_csv():

    user_id = get_jwt_identity()

    bookings = Booking.query.filter_by(user_id=user_id).all()

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "Booking ID",
        "Trek Name",
        "Location",
        "Duration",
        "Booking Date",
        "Status"
    ])

    for booking in bookings:

        trek = Trek.query.get(booking.trek_id)

        writer.writerow([
            booking.id,
            trek.name,
            trek.location,
            trek.duration,
            booking.booking_date,
            booking.status
        ])

    response = make_response(output.getvalue())

    response.headers["Content-Disposition"] = "attachment; filename=trek_history.csv"

    response.headers["Content-Type"] = "text/csv"

    return response

with app.app_context():
    db.create_all()  
    
    admin = User.query.filter_by(username='Naman').first()
    if not admin:
        admin = User(
            user_id='admin001',
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

