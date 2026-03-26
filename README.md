# RIASEC Career Assessment Application

A web-based career assessment tool built with Flask that helps users discover their career interests using the **RIASEC model** (Holland's Theory of Career Choice). The application evaluates users across six personality/interest types and five aptitude categories to provide personalized career guidance.

## What is RIASEC?

RIASEC stands for six personality/interest types:

- **R** – Realistic: Preference for hands-on, practical work
- **I** – Investigative: Interest in research and analytical tasks
- **A** – Artistic: Inclination towards creative and expressive activities
- **S** – Social: Desire to help, teach, or counsel others
- **E** – Enterprising: Drive to lead, persuade, and manage
- **C** – Conventional: Preference for organized, detail-oriented work

## Features

- **User Registration**: Collects user name, occupation, and email before starting the assessment.
- **Interactive Questionnaire**: 30 multiple-choice questions that assess both RIASEC types and aptitudes.
- **Aptitude Scoring**: Measures five aptitude dimensions — Technical, Spatial, Analytical, Creative, and Verbal.
- **Results Dashboard**: Displays RIASEC scores, top 3 career codes, and aptitude breakdown.
- **Persistent Storage**: Stores user data and assessment results in a SQLite database.
- **RESTful API**: Backend API endpoints to start, submit, and retrieve assessment results.
- **Responsive UI**: Clean, modern single-page frontend built with HTML, CSS, and JavaScript.

## Tech Stack

| Component      | Technology         |
|----------------|--------------------|
| Backend        | Python (Flask)     |
| Database       | SQLite (via Flask-SQLAlchemy) |
| Frontend       | HTML, CSS, JavaScript (single-page) |
| CORS Support   | Flask-CORS         |
| Production Server | Gunicorn        |

## Project Structure

```
riasec_app/
├── app.py              # Main Flask application (routes, models, questions)
├── index.html          # Frontend single-page application
├── requirements.txt    # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # Project documentation
```

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/akashkomare/riasec_app.git
   cd riasec_app
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## API Endpoints

| Method | Endpoint                      | Description                          |
|--------|-------------------------------|--------------------------------------|
| GET    | `/`                           | Serves the frontend HTML page        |
| POST   | `/api/start-assessment`       | Registers a user and returns questions |
| POST   | `/api/submit-assessment`      | Submits answers and returns results  |
| GET    | `/api/user-results/<user_id>` | Retrieves all results for a user     |

## How It Works

1. The user fills in their name, occupation, and email to start the assessment.
2. The application presents 30 questions, each with two options mapped to RIASEC types and aptitudes.
3. Upon submission, the backend calculates RIASEC and aptitude scores.
4. The top 3 RIASEC codes are determined and displayed along with detailed score breakdowns.
5. Results are saved to the SQLite database for future retrieval.

## Environment Variables

| Variable | Default | Description              |
|----------|---------|--------------------------|
| `PORT`   | `5000`  | Port for the Flask server |

## License

This project is open source and available for educational and personal use.
