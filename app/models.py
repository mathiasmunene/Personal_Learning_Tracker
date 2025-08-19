from app import db
from datetime import datetime, date

class LearningTopic(db.Model):
    """Model for tracking learning topics"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    target_hours = db.Column(db.Float, default=10.0)  # Default target: 10 hours
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to learning sessions (one-to-many)
    sessions = db.relationship('LearningSession', backref='topic', lazy='dynamic', 
                              cascade='all, delete-orphan')
    
    def total_time_spent(self):
        """Calculate total time spent on this topic"""
        return sum(session.duration for session in self.sessions)
    
    def progress_percentage(self):
        """Calculate progress percentage toward target"""
        if self.target_hours == 0:
            return 0
        return min(100, (self.total_time_spent() / self.target_hours) * 100)
    
    def __repr__(self):
        return f'<LearningTopic {self.name}>'

class LearningSession(db.Model):
    """Model for individual learning sessions"""
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=date.today, nullable=False)
    duration = db.Column(db.Float, nullable=False)  # Duration in hours
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign key to link to LearningTopic
    topic_id = db.Column(db.Integer, db.ForeignKey('learning_topic.id'), nullable=False)
    
    def __repr__(self):
        return f'<LearningSession {self.duration}h on {self.date}>'