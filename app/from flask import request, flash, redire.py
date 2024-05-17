from flask import request, flash, redirect  # Import other necessary modules here
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename():
    i = 1
    while True:
        filename = f"ad{i}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.exists(filepath):
            return filename
        i += 1

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' in request.files:
        image = request.files['image']
        if image.filename == '':
            flash('No image selected')
            return redirect(request.url)
        if image and allowed_file(image.filename):
            filename = generate_unique_filename() + '.' + secure_filename(image.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            image.save(image_path)
            # Add any additional logic you need here
            return 'File uploaded successfully'
    return 'File upload failed'

# Add the route for serving uploaded files here

