from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from models import User, Subject, NoDueStatus, FinalApproval, db
from functools import wraps

student_bp = Blueprint('student', __name__)

def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_role') != 'student':
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@student_bp.route('/dashboard')
@student_required
def dashboard():
    return render_template('student_dashboard.html')

@student_bp.route('/api/subjects')
@student_required
def get_subjects():
    user = User.query.get(session['user_id'])
    subjects = Subject.query.filter_by(
        department=user.department,
        semester=user.semester
    ).all()
    
    subject_data = []
    for subject in subjects:
        status = NoDueStatus.query.filter_by(
            student_id=user.id,
            subject_id=subject.id
        ).first()
        
        subject_data.append({
            'id': subject.id,
            'name': subject.name,
            'status': status.status if status else 'pending',
            'remarks': status.remarks if status else None,
            'updated_at': status.updated_at.strftime('%Y-%m-%d %H:%M') if status and status.updated_at else None
        })
    
    return jsonify(subject_data)

@student_bp.route('/api/final-approval-status')
@student_required
def get_final_approval_status():
    user = User.query.get(session['user_id'])
    final_approval = FinalApproval.query.filter_by(student_id=user.id).first()
    
    # Check if all subjects are approved
    subjects = Subject.query.filter_by(
        department=user.department,
        semester=user.semester
    ).all()
    
    all_approved = True
    for subject in subjects:
        status = NoDueStatus.query.filter_by(
            student_id=user.id,
            subject_id=subject.id
        ).first()
        if not status or status.status != 'approved':
            all_approved = False
            break
    
    return jsonify({
        'can_request': all_approved and not final_approval,
        'status': final_approval.status if final_approval else None,
        'remarks': final_approval.remarks if final_approval else None,
        'updated_at': final_approval.updated_at.strftime('%Y-%m-%d %H:%M') if final_approval and final_approval.updated_at else None
    })

@student_bp.route('/api/request-final-approval', methods=['POST'])
@student_required
def request_final_approval():
    user = User.query.get(session['user_id'])
    
    # Check if already requested
    existing = FinalApproval.query.filter_by(student_id=user.id).first()
    if existing:
        return jsonify({
            'success': False,
            'message': 'Final approval already requested'
        }), 400
    
    # Create final approval request
    final_approval = FinalApproval(student_id=user.id)
    db.session.add(final_approval)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Final approval requested successfully'
    })
