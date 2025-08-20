from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app import db
from app.models import LearningTopic, LearningSession
from datetime import datetime, date
import json

# Create blueprint for routes
main_bp = Blueprint('main', __name__)

# Add this route if it's missing
@main_bp.route('/topic/<int:topic_id>')
def topic_detail(topic_id):
    """Show details for a specific topic"""
    topic = LearningTopic.query.get_or_404(topic_id)
    today = date.today().isoformat()  # Get today's date in YYYY-MM-DD format
    return render_template('topic_detail.html', topic=topic, today=today)

@main_bp.route('/')
def index():
    """Home page with overview of learning progress"""
    topics = LearningTopic.query.all()
    
    # Calculate overall statistics
    total_time = sum(topic.total_time_spent() for topic in topics)
    total_sessions = LearningSession.query.count()
    
    return render_template('index.html', 
                         topics=topics, 
                         total_time=total_time, 
                         total_sessions=total_sessions)

@main_bp.route('/dashboard')
def dashboard():
    """Dashboard with visual progress charts"""
    topics = LearningTopic.query.all()
    
    # Prepare data for charts
    topic_names = [topic.name for topic in topics]
    time_spent = [topic.total_time_spent() for topic in topics]
    progress = [topic.progress_percentage() for topic in topics]
    
    return render_template('dashboard.html',
                         topic_names=json.dumps(topic_names),
                         time_spent=json.dumps(time_spent),
                         progress=json.dumps(progress))

@main_bp.route('/topic/add', methods=['GET', 'POST'])
def add_topic():
    """Add a new learning topic"""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        target_hours = float(request.form.get('target_hours', 10))
        
        # Create new topic
        new_topic = LearningTopic(
            name=name,
            description=description,
            target_hours=target_hours
        )
        
        db.session.add(new_topic)
        db.session.commit()
        
        flash(f'Topic "{name}" added successfully!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('add_topic.html')

@main_bp.route('/topic/<int:topic_id>')
def topic_detail(topic_id):
    """Show details for a specific topic"""
    topic = LearningTopic.query.get_or_404(topic_id)
    return render_template('topic_detail.html', topic=topic)

@main_bp.route('/session/add', methods=['POST'])
def add_session():
    """Add a learning session for a topic"""
    topic_id = request.form.get('topic_id')
    duration = float(request.form.get('duration'))
    notes = request.form.get('notes')
    session_date = request.form.get('date') or date.today()
    
    # Convert string date to date object if needed
    if isinstance(session_date, str):
        session_date = datetime.strptime(session_date, '%Y-%m-%d').date()
    
    # Create new session
    new_session = LearningSession(
        topic_id=topic_id,
        duration=duration,
        notes=notes,
        date=session_date
    )
    
    db.session.add(new_session)
    db.session.commit()
    
    flash('Learning session added successfully!', 'success')
    return redirect(url_for('main.topic_detail', topic_id=topic_id))

@main_bp.route('/api/topics')
def api_topics():
    """API endpoint to get topics data (for AJAX requests)"""
    topics = LearningTopic.query.all()
    result = []
    
    for topic in topics:
        result.append({
            'id': topic.id,
            'name': topic.name,
            'time_spent': topic.total_time_spent(),
            'progress': topic.progress_percentage(),
            'target_hours': topic.target_hours
        })
    
    return jsonify(result)