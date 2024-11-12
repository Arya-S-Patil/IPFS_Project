import os
import requests
from flask import Flask, render_template, request, redirect, url_for, flash

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'txt', 'pdf'}
app.secret_key = 'your_secret_key'  # Replace with your actual secret key for session management

# IPFS API URL
IPFS_API_URL = 'http://localhost:5001/api/v0/'  # IPFS Node API URL
IPFS_CLUSTER_API_URL = 'http://localhost:9094/pins/'  # IPFS Cluster API URL for pinning

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Route to upload file to IPFS and Pin to IPFS Cluster
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Step 1: Upload the file to IPFS using IPFS node API
            try:
                with open(filepath, 'rb') as f:
                    files = {'file': (filename, f)}
                    ipfs_response = requests.post(f'{IPFS_API_URL}add', files=files)

                if ipfs_response.status_code == 200:
                    ipfs_hash = ipfs_response.json()['Hash']
                    flash(f'File uploaded successfully to IPFS. IPFS Hash: {ipfs_hash}', 'success')

                    # Step 2: Pin the file to IPFS Cluster using IPFS Cluster API
                    pin_response = requests.post(f'{IPFS_CLUSTER_API_URL}{ipfs_hash}')

                    if pin_response.status_code == 200:
                        flash(f'File pinned to IPFS Cluster successfully.', 'success')
                        return redirect(url_for('view_file', ipfs_hash=ipfs_hash))  # Redirect to view file
                    else:
                        flash(f"Error pinning file to IPFS Cluster: {pin_response.text}", 'danger')
                        return redirect(request.url)

                else:
                    flash(f"Error uploading file to IPFS: {ipfs_response.text}", 'danger')
                    return redirect(request.url)

            except Exception as e:
                flash(f"Error uploading file to IPFS or IPFS Cluster: {str(e)}", 'danger')
                return redirect(request.url)
    return render_template('index.html')

# Route to view the uploaded file via the local IPFS gateway
@app.route('/file/<ipfs_hash>')
def view_file(ipfs_hash):
    # Create the local IPFS URL to view the file via the IPFS gateway
    file_url = f'http://localhost:8080/ipfs/{ipfs_hash}'  # Local IPFS gateway URL
    return render_template('view_file.html', file_url=file_url)

# Home route
@app.route('/')
def index():
    return redirect(url_for('upload_file'))

if __name__ == '__main__':
    app.run(debug=True)
