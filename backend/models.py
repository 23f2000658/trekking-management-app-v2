from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    """Unified User model for Admin, Staff, and Trekkers"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), unique=True, nullable=False )
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')  
    is_active = db.Column(db.Boolean, default=True) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

   
    bookings = db.relationship('Booking', backref='user', cascade="all, delete-orphan", lazy=True)
    assigned_treks = db.relationship(
        'Trek', 
        backref='staff', 
        lazy=True,
        primaryjoin="User.user_id == Trek.staff_id", 
        foreign_keys="[Trek.staff_id]"             
    )

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'


class Trek(db.Model):
    """Trek model"""
    __tablename__ = 'treks'
    
    id = db.Column(db.Integer, primary_key=True)
    trek_id = db.Column(db.String(80), unique=True, nullable=False )
    name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)  
    duration = db.Column(db.Integer, nullable=False)  
    total_slots = db.Column(db.Integer, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='Open')  
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    staff_id = db.Column(db.String(50), nullable=True)
    
    
    bookings = db.relationship('Booking', backref='trek', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Trek {self.name}>'


class Booking(db.Model):
    """Booking model for Users"""
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey('treks.id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Booked') 
    
    def __repr__(self):
        return f'<Booking {self.id} - User {self.user_id}>'