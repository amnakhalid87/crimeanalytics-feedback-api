from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///feedback.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Database Model
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Text, nullable=False)
    message = db.Column(db.Text, nullable=False)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def home():
    return jsonify({
        'message': 'Feedback API is working!',
        'endpoints': {
            'POST /feedback': 'Submit feedback',
            'GET /feedback': 'Get all feedback',
            'GET /feedback/<user_id>': 'Get feedback by user ID'
        }
    })

@app.route('/feedback', methods=['POST'])
def save_feedback():
    """Save feedback from frontend"""
    try:
        data = request.get_json()
        
        if not data or 'user_id' not in data or 'message' not in data:
            return jsonify({'error': 'Missing user_id or message'}), 400
        
        feedback = Feedback(
            user_id=data['user_id'],
            message=data['message']
        )

        db.session.add(feedback)
        db.session.commit()

        return jsonify({'message': 'Feedback saved'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/feedback', methods=['GET'])
def get_all_feedback():
    """Get all feedback messages"""
    try:
        feedback_list = Feedback.query.all()

        result = []
        for feedback in feedback_list:
            result.append({
                'id': feedback.id,
                'user_id': feedback.user_id,
                'message': feedback.message
            })

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/feedback/<user_id>', methods=['GET'])
def get_user_feedback(user_id):
    """Get feedback by user ID"""
    try:
        feedback_list = Feedback.query.filter_by(user_id=user_id).all()

        result = []
        for feedback in feedback_list:
            result.append({
                'id': feedback.id,
                'user_id': feedback.user_id,
                'message': feedback.message
            })

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
