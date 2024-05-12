# need to create a static/uplaods folder by using mkdir static then mkdir static/uploads 
#then this code used to update the current routes.py 
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if 'image' in request.files:
        image = request.files['image']
        if image.filename == '':
            flash('No image selected')
            return redirect(request.url)
        if image and allowed_file(image.filename):
            filename = str(uuid.uuid4()) + '.' + secure_filename(image.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            image.save(image_path)
            form_data.append(filename)