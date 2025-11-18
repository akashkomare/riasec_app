from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import uuid
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///riasec_assessment.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

# Database Models
class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    occupation = db.Column(db.String(100))
    email = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AssessmentResult(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    riasec_scores = db.Column(db.JSON, nullable=False)
    aptitude_scores = db.Column(db.JSON, nullable=False)
    top_codes = db.Column(db.JSON, nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('results', lazy=True))

# Complete questions data
QUESTIONS = [
    {
        "number": 1,
        "question": "Which activity would you prefer?",
        "options": {
            "A": {"text": "Build and repair mechanical devices", "riasec": "R", "aptitudes": {"Technical": 1, "Spatial": 1}},
            "B": {"text": "Research scientific problems", "riasec": "I", "aptitudes": {"Analytical": 1}}
        }
    },
    {
        "number": 2,
        "question": "Which work environment appeals to you more?",
        "options": {
            "A": {"text": "Working with your hands on practical projects", "riasec": "R", "aptitudes": {"Technical": 1, "Spatial": 1}},
            "B": {"text": "Creating artistic works or performances", "riasec": "A", "aptitudes": {"Creative": 1, "Spatial": 1}}
        }
    },
    {
        "number": 3,
        "question": "Which type of work interests you more?",
        "options": {
            "A": {"text": "Teaching or counseling people", "riasec": "S", "aptitudes": {"Verbal": 1}},
            "B": {"text": "Leading a team or managing projects", "riasec": "E", "aptitudes": {"Analytical": 1, "Verbal": 1}}
        }
    },
    {
        "number": 4,
        "question": "What kind of tasks do you prefer?",
        "options": {
            "A": {"text": "Organizing data and maintaining records", "riasec": "C", "aptitudes": {"Analytical": 1}},
            "B": {"text": "Conducting experiments and analyzing results", "riasec": "I", "aptitudes": {"Analytical": 1, "Technical": 1}}
        }
    },
    {
        "number": 5,
        "question": "Which activity sounds more appealing?",
        "options": {
            "A": {"text": "Writing creative stories or designing graphics", "riasec": "A", "aptitudes": {"Creative": 1, "Verbal": 1}},
            "B": {"text": "Helping people solve personal problems", "riasec": "S", "aptitudes": {"Analytical": 1, "Verbal": 1}}
        }
    },
    {
        "number": 6,
        "question": "What type of work environment do you prefer?",
        "options": {
            "A": {"text": "Selling products or persuading others", "riasec": "E", "aptitudes": {"Verbal": 1}},
            "B": {"text": "Following detailed procedures and protocols", "riasec": "C", "aptitudes": {"Analytical": 1, "Technical": 1}}
        }
    },
    {
        "number": 7,
        "question": "Which would you rather do?",
        "options": {
            "A": {"text": "Operate machinery or tools", "riasec": "R", "aptitudes": {"Technical": 1, "Spatial": 1}},
            "B": {"text": "Perform on stage or create art", "riasec": "A", "aptitudes": {"Creative": 1, "Spatial": 1}}
        }
    },
    {
        "number": 8,
        "question": "Which work style suits you better?",
        "options": {
            "A": {"text": "Studying complex problems and theories", "riasec": "I", "aptitudes": {"Analytical": 1}},
            "B": {"text": "Working with people in groups", "riasec": "S", "aptitudes": {"Verbal": 1}}
        }
    },
    {
        "number": 9,
        "question": "What type of responsibility interests you?",
        "options": {
            "A": {"text": "Managing business operations", "riasec": "E", "aptitudes": {"Analytical": 1, "Verbal": 1}},
            "B": {"text": "Building or fixing things", "riasec": "R", "aptitudes": {"Technical": 1, "Spatial": 1}}
        }
    },
    {
        "number": 10,
        "question": "Which work activity do you prefer?",
        "options": {
            "A": {"text": "Keeping accurate financial records", "riasec": "C", "aptitudes": {"Analytical": 1}},
            "B": {"text": "Creating innovative solutions", "riasec": "I", "aptitudes": {"Creative": 1, "Analytical": 1}}
        }
    },
    {
        "number": 11,
        "question": "Which environment appeals to you more?",
        "options": {
            "A": {"text": "Working outdoors with tools and equipment", "riasec": "R", "aptitudes": {"Technical": 1, "Spatial": 1}},
            "B": {"text": "Working in a laboratory or research facility", "riasec": "I", "aptitudes": {"Analytical": 1, "Technical": 1}}
        }
    },
    {
        "number": 12,
        "question": "What kind of work energizes you?",
        "options": {
            "A": {"text": "Expressing yourself through creative media", "riasec": "A", "aptitudes": {"Creative": 1, "Spatial": 1}},
            "B": {"text": "Helping others learn and grow", "riasec": "S", "aptitudes": {"Verbal": 1, "Analytical": 1}}
        }
    },
    {
        "number": 13,
        "question": "Which role would you prefer?",
        "options": {
            "A": {"text": "Leading business ventures and negotiations", "riasec": "E", "aptitudes": {"Verbal": 1, "Analytical": 1}},
            "B": {"text": "Organizing systems and processes", "riasec": "C", "aptitudes": {"Analytical": 1, "Technical": 1}}
        }
    },
    {
        "number": 14,
        "question": "What type of problem-solving do you enjoy?",
        "options": {
            "A": {"text": "Hands-on mechanical troubleshooting", "riasec": "R", "aptitudes": {"Technical": 1, "Spatial": 1, "Analytical": 1}},
            "B": {"text": "Theoretical and abstract analysis", "riasec": "I", "aptitudes": {"Analytical": 1}}
        }
    },
    {
        "number": 15,
        "question": "Which work focus interests you more?",
        "options": {
            "A": {"text": "Creating visual or performing arts", "riasec": "A", "aptitudes": {"Creative": 1, "Spatial": 1}},
            "B": {"text": "Providing care and support to others", "riasec": "S", "aptitudes": {"Verbal": 1}}
        }
    },
    {
        "number": 16,
        "question": "What motivates you most?",
        "options": {
            "A": {"text": "Achieving business goals and targets", "riasec": "E", "aptitudes": {"Analytical": 1, "Verbal": 1}},
            "B": {"text": "Maintaining order and accuracy", "riasec": "C", "aptitudes": {"Analytical": 1}}
        }
    },
    {
        "number": 17,
        "question": "Which work style suits you?",
        "options": {
            "A": {"text": "Working with physical materials and tools", "riasec": "R", "aptitudes": {"Technical": 1, "Spatial": 1}},
            "B": {"text": "Working with ideas and concepts", "riasec": "I", "aptitudes": {"Analytical": 1}}
        }
    },
    {
        "number": 18,
        "question": "What kind of work environment do you prefer?",
        "options": {
            "A": {"text": "Creative and expressive atmosphere", "riasec": "A", "aptitudes": {"Creative": 1, "Spatial": 1}},
            "B": {"text": "Collaborative and people-focused environment", "riasec": "S", "aptitudes": {"Verbal": 1}}
        }
    },
    {
        "number": 19,
        "question": "Which responsibility appeals to you?",
        "options": {
            "A": {"text": "Influencing and directing others", "riasec": "E", "aptitudes": {"Verbal": 1, "Analytical": 1}},
            "B": {"text": "Following established procedures", "riasec": "C", "aptitudes": {"Analytical": 1, "Technical": 1}}
        }
    },
    {
        "number": 20,
        "question": "What type of tasks energize you?",
        "options": {
            "A": {"text": "Building, repairing, or constructing", "riasec": "R", "aptitudes": {"Technical": 1, "Spatial": 1}},
            "B": {"text": "Researching and discovering new knowledge", "riasec": "I", "aptitudes": {"Analytical": 1}}
        }
    },
    {
        "number": 21,
        "question": "Which work focus interests you more?",
        "options": {
            "A": {"text": "Artistic expression and creativity", "riasec": "A", "aptitudes": {"Creative": 1, "Spatial": 1}},
            "B": {"text": "Community service and helping others", "riasec": "S", "aptitudes": {"Verbal": 1, "Analytical": 1}}
        }
    },
    {
        "number": 22,
        "question": "What drives your work satisfaction?",
        "options": {
            "A": {"text": "Leading teams and making decisions", "riasec": "E", "aptitudes": {"Verbal": 1, "Analytical": 1}},
            "B": {"text": "Managing details and data accurately", "riasec": "C", "aptitudes": {"Analytical": 1}}
        }
    },
    {
        "number": 23,
        "question": "Which work environment do you prefer?",
        "options": {
            "A": {"text": "Practical, hands-on workshop settings", "riasec": "R", "aptitudes": {"Technical": 1, "Spatial": 1}},
            "B": {"text": "Intellectual, research-oriented settings", "riasec": "I", "aptitudes": {"Analytical": 1, "Technical": 1}}
        }
    },
    {
        "number": 24,
        "question": "What type of work appeals to you?",
        "options": {
            "A": {"text": "Creating original artistic works", "riasec": "A", "aptitudes": {"Creative": 1, "Spatial": 1}},
            "B": {"text": "Supporting and teaching others", "riasec": "S", "aptitudes": {"Verbal": 1, "Analytical": 1}}
        }
    },
    {
        "number": 25,
        "question": "Which role would you choose?",
        "options": {
            "A": {"text": "Persuading and selling to others", "riasec": "E", "aptitudes": {"Verbal": 1}},
            "B": {"text": "Organizing and systematizing information", "riasec": "C", "aptitudes": {"Analytical": 1, "Technical": 1}}
        }
    },
    {
        "number": 26,
        "question": "What motivates you in work?",
        "options": {
            "A": {"text": "Working with machines and technology", "riasec": "R", "aptitudes": {"Technical": 1, "Spatial": 1}},
            "B": {"text": "Solving complex theoretical problems", "riasec": "I", "aptitudes": {"Analytical": 1}}
        }
    },
    {
        "number": 27,
        "question": "Which work style suits you better?",
        "options": {
            "A": {"text": "Free-form creative expression", "riasec": "A", "aptitudes": {"Creative": 1, "Spatial": 1}},
            "B": {"text": "Interpersonal helping and support", "riasec": "S", "aptitudes": {"Verbal": 1}}
        }
    },
    {
        "number": 28,
        "question": "What type of responsibility interests you?",
        "options": {
            "A": {"text": "Business leadership and management", "riasec": "E", "aptitudes": {"Verbal": 1, "Analytical": 1}},
            "B": {"text": "Administrative coordination and control", "riasec": "C", "aptitudes": {"Analytical": 1, "Technical": 1}}
        }
    },
    {
        "number": 29,
        "question": "Which work focus energizes you?",
        "options": {
            "A": {"text": "Physical construction and repair work", "riasec": "R", "aptitudes": {"Technical": 1, "Spatial": 1}},
            "B": {"text": "Scientific investigation and research", "riasec": "I", "aptitudes": {"Analytical": 1, "Technical": 1}}
        }
    },
    {
        "number": 30,
        "question": "What kind of work environment do you prefer?",
        "options": {
            "A": {"text": "Creative studios and artistic spaces", "riasec": "A", "aptitudes": {"Creative": 1, "Spatial": 1}},
            "B": {"text": "People-centered service environments", "riasec": "S", "aptitudes": {"Verbal": 1}}
        }
    }
]

# Initialize database
with app.app_context():
    db.create_all()

# Serve the frontend
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

# API Routes
@app.route('/api/start-assessment', methods=['POST'])
def start_assessment():
    """Register user and start assessment"""
    try:
        data = request.json
        user = User(
            name=data.get('name'),
            occupation=data.get('occupation'),
            email=data.get('email')
        )
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'user_id': user.id,
            'message': 'Assessment started successfully',
            'questions': QUESTIONS
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/submit-assessment', methods=['POST'])
def submit_assessment():
    """Submit assessment answers and calculate results"""
    try:
        data = request.json
        user_id = data.get('user_id')
        answers = data.get('answers', {})
        
        # Calculate scores
        riasec_scores = {"R": 0, "I": 0, "A": 0, "S": 0, "E": 0, "C": 0}
        aptitude_scores = {"Technical": 0, "Spatial": 0, "Analytical": 0, "Creative": 0, "Verbal": 0}
        
        for question_num, answer in answers.items():
            question = next((q for q in QUESTIONS if q['number'] == int(question_num)), None)
            if question and answer in question['options']:
                option_data = question['options'][answer]
                # Add to RIASEC score
                riasec_scores[option_data['riasec']] += 1
                # Add to aptitude scores
                for aptitude, score in option_data['aptitudes'].items():
                    aptitude_scores[aptitude] += score
        
        # Get top 3 RIASEC codes
        sorted_riasec = sorted(riasec_scores.items(), key=lambda x: x[1], reverse=True)
        top_codes = [code for code, score in sorted_riasec[:3]]
        
        # Save results
        result = AssessmentResult(
            user_id=user_id,
            riasec_scores=riasec_scores,
            aptitude_scores=aptitude_scores,
            top_codes=top_codes
        )
        db.session.add(result)
        db.session.commit()
        
        return jsonify({
            'results': {
                'riasec_scores': riasec_scores,
                'aptitude_scores': aptitude_scores,
                'top_codes': top_codes
            },
            'result_id': result.id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user-results/<user_id>', methods=['GET'])
def get_user_results(user_id):
    """Get all assessment results for a user"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        results = []
        for result in user.results:
            results.append({
                'id': result.id,
                'riasec_scores': result.riasec_scores,
                'aptitude_scores': result.aptitude_scores,
                'top_codes': result.top_codes,
                'completed_at': result.completed_at.isoformat()
            })
        
        return jsonify({
            'user': {
                'name': user.name,
                'occupation': user.occupation,
                'email': user.email
            },
            'results': results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=port)