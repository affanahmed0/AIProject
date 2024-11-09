from demo import ask_chatgpt
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import openai
app = Flask(__name__)

# Set secret key for session management
app.secret_key = 'your_secret_key_here'

# Database configuration (using SQLite for simplicity)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Set up your OpenAI API key
openai.api_key = 'your-openai-api-key-here'

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    quizzes_completed = db.Column(db.Integer, default=0)
    total_score = db.Column(db.Integer, default=0)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    max_score = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    score = db.Column(db.Integer, nullable=False)

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = username
            session['user_id'] = user.id  # Store user ID in session
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials. Please try again."
    
    return render_template('login.html')
@app.route( )

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))  # Redirect after successful signup
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('login'))


# ChatGPT Route
@app.route('/ask_chatgpt', methods=['GET', 'POST'])
def ask_chatgpt():
    if request.method == 'POST':
        prompt = request.form['prompt']  # Get the prompt from the form input
        
        # Generate response using OpenAI's GPT-3
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            temperature=0.5
        )
        result = response.choices[0].text.strip()
        
        # Render the response back to the user
        return render_template('ask_chatgpt.html', result=result)
    
    # On GET request, just display the input form
    return render_template('ask_chatgpt.html')

# Submit Quiz Route
@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    score = request.form['score']
    student_id = session.get('user_id')
    quiz_id = request.form['quiz_id']
    
    quiz = Quiz.query.get(quiz_id)
    user = User.query.get(student_id)
    
    if user and quiz:
        user.total_score += int(score)
        user.quizzes_completed += 1
        db.session.commit()
    
    return redirect(url_for('dashboard'))

@app.route('/profile')
def profile():
    if 'username' in session:
        user = User.query.get(session['user_id'])
        return render_template('profile.html', user=user)
    else:
        return redirect(url_for('login'))

# Progress Tracking
@app.route('/progress')
def progress():
    if 'username' in session:
        progress_data = {
            'total_quizzes': 20,
            'completed_quizzes': 15,
            'total_games': 10,
            'played_games': 6
        }
        return render_template('progress.html', progress=progress_data)
    else:
        return redirect(url_for('login'))

@app.route('/quizzes')
def quizzes():
    if 'username' in session:
        quizzes = Quiz.query.all()
        return render_template('quizzes.html', quizzes=quizzes)
    return redirect(url_for('login'))

@app.route('/games')
def games():
    if 'username' in session:
        games = [
            {'title': 'Math Puzzle', 'description': 'Solve puzzles to unlock levels'},
            {'title': 'Abacus Game', 'description': 'Use abacus to solve arithmetic problems'}
        ]
        return render_template('games.html', games=games)
    return redirect(url_for('login'))

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        user.username = request.form['username']
        db.session.commit()
        return redirect(url_for('profile'))  # Redirect to profile after editing

    return render_template('edit_profile.html', user=user)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
        
        # Check if test user already exists
        if not User.query.filter_by(username='testuser').first():
            # Create a test user
            test_user = User(username='testuser', password='password123')
            db.session.add(test_user)
            db.session.commit()
            print("Test user 'testuser' has been created.")
        else:
            print("Test user already exists.")
    
    app.run(debug=True)
