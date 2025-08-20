from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)


# Database Model
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Text, nullable=False)
    message = db.Column(db.Text, nullable=False)


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
    data = request.get_json()

    feedback = Feedback(
        user_id=data['user_id'],
        message=data['message']
    )

    db.session.add(feedback)
    db.session.commit()

    return jsonify({'message': 'Feedback saved'})


@app.route('/feedback', methods=['GET'])
def get_all_feedback():
    """Get all feedback messages"""
    feedback_list = Feedback.query.all()

    result = []
    for feedback in feedback_list:
        result.append({
            'id': feedback.id,
            'user_id': feedback.user_id,
            'message': feedback.message
        })

    return jsonify(result)


@app.route('/feedback/<int:user_id>', methods=['GET'])
def get_user_feedback(user_id):
    """Get feedback by user ID"""
    feedback_list = Feedback.query.filter_by(user_id=user_id).all()

    result = []
    for feedback in feedback_list:
        result.append({
            'id': feedback.id,
            'user_id': feedback.user_id,
            'message': feedback.message
        })

    return jsonify(result)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))