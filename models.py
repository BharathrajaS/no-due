from extensions import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # student, staff, hod
    department = db.Column(db.String(50), nullable=False)
    class_section = db.Column(db.String(10))  # A or B
    year = db.Column(db.Integer)  # For students
    semester = db.Column(db.Integer)  # For students
    roll_number = db.Column(db.String(20))  # For students
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # e.g., "CSE 1st Year Section A"
    department = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    section = db.Column(db.String(10), nullable=False)  # A, B, C, etc.
    class_advisor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    class_advisor = db.relationship('User', backref='advised_classes')

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), nullable=False)  # Subject code like CS101
    department = db.Column(db.String(50), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    credits = db.Column(db.Integer, default=3)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    assigned_class = db.relationship('Class', backref='subjects')

class StaffSubject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    staff = db.relationship('User', backref='staff_subjects')
    subject = db.relationship('Subject', backref='staff_assignments')
    assigned_class = db.relationship('Class', backref='staff_assignments')

class NoDueStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    approved_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    student = db.relationship('User', foreign_keys=[student_id], backref='no_due_statuses')
    subject = db.relationship('Subject', backref='no_due_statuses')
    approver = db.relationship('User', foreign_keys=[approved_by])

class FinalApproval(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    approved_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    student = db.relationship('User', foreign_keys=[student_id], backref='final_approvals')
    approver = db.relationship('User', foreign_keys=[approved_by])
