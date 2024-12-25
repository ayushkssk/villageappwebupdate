from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pratappur.db'
app.config['SECRET_KEY'] = 'your-secret-key'  # Change this in production
db = SQLAlchemy(app)

# Database Models
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    new_feedback = Feedback(
        name=data['name'],
        message=data['message']
    )
    db.session.add(new_feedback)
    db.session.commit()
    return jsonify({"message": "फीडबैक के लिए धन्यवाद!"})

@app.route('/get-feedback')
def get_feedback():
    feedbacks = Feedback.query.order_by(Feedback.date.desc()).all()
    return jsonify([{
        'name': f.name,
        'message': f.message,
        'date': f.date.strftime('%Y-%m-%d %H:%M:%S')
    } for f in feedbacks])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
