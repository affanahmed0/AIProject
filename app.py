from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # For session management

# Mock user data (You'd replace this with a proper database)
users = {"testuser": "password123"}

@app.route('/')
def home():
    # Redirect to login if the user is not authenticated
    if 'username' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Authenticate user
        if username in users and users[username] == password:
            session['username'] = username  # Store the user's session
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials, try again."
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Add new user to mock database
        users[username] = password
        session['username'] = username
        return redirect(url_for('dashboard'))
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    # Ensure the user is logged in
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/ask', methods=['POST'])
def ask():
    query = request.form['query']
    # Call your AI function to handle the query here
    response = "AI response for the query: " + query
    return render_template('dashboard.html', query=query, response=response)

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove the user's session
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

