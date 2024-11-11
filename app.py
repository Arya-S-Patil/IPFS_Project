from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Sample data for demonstration
users = {'testuser': 'password123'}
user_files = {
    'testuser': [
        {'filename': 'file1.txt', 'cid': 'QmExampleHash1'},
        {'filename': 'file2.jpg', 'cid': 'QmExampleHash2'}
    ]
}

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials, please try again."
    return render_template('home.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('home'))
    
    username = session['username']
    user_files_list = user_files.get(username, [])
    
    if request.method == 'POST':
        search_query = request.form['search']
        filtered_files = [f for f in user_files_list if search_query in f['filename']]
        return render_template('dashboard.html', files=filtered_files, username=username)

    return render_template('dashboard.html', files=user_files_list, username=username)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'username' not in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        # Logic to handle file upload goes here
        return redirect(url_for('dashboard'))

    return render_template('upload.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

