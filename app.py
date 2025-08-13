from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from extensions import db
from blueprints.auth import auth_bp



app = Flask(__name__)
app.config['SECRET_KEY'] = 's8d7f6s8d7f6s8d7f6s8d7f6!@#%GHSDFhwefhwe'
app.config['SQLALCHEMY_DATABASE_URI'] =  'postgresql://neondb_owner:npg_08SDhaoFsubI@ep-orange-cell-ab67h29b-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Import models
from models import User, Subject, StaffSubject, NoDueStatus, FinalApproval, Class

# Import blueprints
from blueprints.auth import auth_bp
from blueprints.student import student_bp
from blueprints.staff import staff_bp
from blueprints.hod import hod_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(student_bp, url_prefix='/student')
app.register_blueprint(staff_bp, url_prefix='/staff')
app.register_blueprint(hod_bp, url_prefix='/hod')

@app.route('/')
def index():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user is None:
            # User not found, clear session and redirect to login
            session.pop('user_id', None)
            return redirect(url_for('login'))
        if user.role == 'student':
            return redirect(url_for('student.dashboard'))
        elif user.role == 'staff':
            return redirect(url_for('staff.dashboard'))
        elif user.role == 'hod':
            return redirect(url_for('hod.dashboard'))
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

def create_sample_data():
    # Create sample HOD
    if not User.query.filter_by(role='hod').first():
        hod = User(
            name='Dr. John Smith',
            email='hod@college.edu',
            password=generate_password_hash('password123'),
            role='hod',
            department='CSE',
            class_section='A',
            year=None,
            semester=None,
            roll_number=None
        )
        db.session.add(hod)
        db.session.commit()
    
    # Create sample classes
    if not Class.query.first():
        classes = [
            Class(name='CSE 1st Year Section A', department='CSE', year=1, semester=1, section='A'),
            Class(name='CSE 1st Year Section B', department='CSE', year=1, semester=1, section='B'),
            Class(name='CSE 2nd Year Section A', department='CSE', year=2, semester=3, section='A'),
            Class(name='CSE 2nd Year Section B', department='CSE', year=2, semester=3, section='B'),
        ]
        for cls in classes:
            db.session.add(cls)
        db.session.commit()
    
    # Create sample subjects
    if not Subject.query.first():
        # Get the first class for assignment
        first_class = Class.query.first()
        subjects = [
            Subject(name='Mathematics', code='MATH101', department='CSE', semester=1, credits=4, class_id=first_class.id if first_class else None),
            Subject(name='Physics', code='PHY101', department='CSE', semester=1, credits=3, class_id=first_class.id if first_class else None),
            Subject(name='Chemistry', code='CHEM101', department='CSE', semester=1, credits=3, class_id=first_class.id if first_class else None),
            Subject(name='Programming', code='CS101', department='CSE', semester=1, credits=4, class_id=first_class.id if first_class else None),
            Subject(name='English', code='ENG101', department='CSE', semester=1, credits=2, class_id=first_class.id if first_class else None)
        ]
        for subject in subjects:
            db.session.add(subject)
        db.session.commit()
        
if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
        create_sample_data()
        app.run(debug=True)
