from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from models import User, Subject, StaffSubject, NoDueStatus, db
from functools import wraps

staff_bp = Blueprint('staff', __name__)

def staff_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_role') not in ['staff', 'hod']:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@staff_bp.route('/dashboard')
@staff_required
def dashboard():
    return render_template('staff_dashboard.html')

@staff_bp.route('/api/assigned-subjects')
@staff_required
def get_assigned_subjects():
    staff_id = session['user_id']
    assignments = StaffSubject.query.filter_by(staff_id=staff_id).all()
    
    subjects_data = []
    for assignment in assignments:
        subjects_data.append({
            'id': assignment.subject.id,
            'name': assignment.subject.name,
            'class_section': assignment.assigned_class.section,
            'department': assignment.subject.department,
            'semester': assignment.subject.semester
        })
    
    return jsonify(subjects_data)

@staff_bp.route('/api/students/<int:subject_id>/<class_section>')
@staff_required
def get_students_for_subject(subject_id, class_section):
    subject = Subject.query.get_or_404(subject_id)
    
    students = User.query.filter_by(
        role='student',
        department=subject.department,
        semester=subject.semester,
        class_section=class_section
    ).all()
    
    students_data = []
    for student in students:
        status = NoDueStatus.query.filter_by(
            student_id=student.id,
            subject_id=subject_id
        ).first()
        
        students_data.append({
            'id': student.id,
            'name': student.name,
            'roll_number': student.roll_number,
            'status': status.status if status else 'pending',
            'remarks': status.remarks if status else None,
            'updated_at': status.updated_at.strftime('%Y-%m-%d %H:%M') if status and status.updated_at else None
        })
    
    return jsonify(students_data)

@staff_bp.route('/api/approve-student', methods=['POST'])
@staff_required
def approve_student():
    data = request.get_json()
    student_id = data.get('student_id')
    subject_id = data.get('subject_id')
    action = data.get('action')  # approve or reject
    remarks = data.get('remarks', '')
    
    # Check if status already exists
    status = NoDueStatus.query.filter_by(
        student_id=student_id,
        subject_id=subject_id
    ).first()
    
    if status:
        status.status = 'approved' if action == 'approve' else 'rejected'
        status.approved_by = session['user_id']
        status.remarks = remarks
    else:
        status = NoDueStatus(
            student_id=student_id,
            subject_id=subject_id,
            status='approved' if action == 'approve' else 'rejected',
            approved_by=session['user_id'],
            remarks=remarks
        )
        db.session.add(status)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'Student {action}d successfully'
    })
