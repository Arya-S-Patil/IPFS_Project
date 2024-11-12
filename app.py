from flask import Flask, request, render_template, redirect, url_for, session
import ipfshttpclient

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Essential for session handling
client = ipfshttpclient.connect()  # Connect to the local IPFS daemon

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Simplified authentication (adjust for production)
        if username == 'testuser' and password == 'password123':
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials. Please try again."
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        search_query = request.form['search']
        return redirect(url_for('view_file', hash=search_query))

    return render_template('dashboard.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        file = request.files['file']
        if file:
            result = client.add(file)
            return render_template('dashboard.html', file_hash=result['Hash'], success=True)
    return render_template('upload.html')

@app.route('/view/<hash>')
def view_file(hash):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    try:
        file_content = client.cat(hash)
        if isinstance(file_content, bytes):
            return render_template('view.html', file_hash=hash, file_type='binary')
        else:
            return render_template('view.html', file_content=file_content.decode('utf-8', errors='replace'), file_hash=hash)
    except Exception as e:
        return f'Error retrieving file: {str(e)}'

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
