from flask import Blueprint, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    user = User.query.filter_by(email=email).first()
    
    if user and user.password == password:
        session['user_id'] = user.id
        session['user_role'] = user.role
        session['user_name'] = user.name
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'role': user.role,
            'redirect': f'/{user.role}/dashboard'
        })
    
    return jsonify({
        'success': False,
        'message': 'Invalid email or password'
    }), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Check if user already exists
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({
            'success': False,
            'message': 'Email already registered'
        }), 400
    
    # Create new user
    user = User(
        name=data.get('name'),
        email=data.get('email'),
        password=data.get('password'),
        role=data.get('role'),
        department=data.get('department'),
        class_section=data.get('class_section'),
        year=data.get('year') if data.get('role') == 'student' else None,
        semester=data.get('semester') if data.get('role') == 'student' else None,
        roll_number=data.get('roll_number') if data.get('role') == 'student' else None
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Registration successful'
    })

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({
        'success': True,
        'message': 'Logged out successfully'
    })
