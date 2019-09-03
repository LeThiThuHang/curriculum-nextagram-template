from flask import Blueprint, render_template, flash, request,redirect, url_for
from models.user import User
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_required, current_user
import re
from werkzeug.utils import secure_filename
from app import app

from helpers import s3, DevelopmentConfig, upload_file_to_s3





edits_blueprint = Blueprint('users/edit',
                            __name__,
                            template_folder='templates')

#this is to show the edit form
@edits_blueprint.route('/<userid>')
def new(userid):
    #only render template if the current user is login from layout
    return render_template('edits/edit.html')

# this is to take in new user information to the database
@edits_blueprint.route('/<id>', methods=['POST'])
@login_required
def edit(id):
    user = User.get_by_id(id)

    if current_user.id == user.id:

        change_name = request.form['name']
        change_email = request.form['email']
        change_password = request.form['password']

        if change_name != user.name:
            user.name = change_name
        if change_email != user.email:
            user.email = change_email
        if len(change_password) > 1: 
            user.password =change_password

        if user.save():
            flash('Your account is updated succesfully','success') 
            return render_template('home.html')
        else:
            flash('Fail to update', 'danger')
            return render_template('edits/edit.html', userid = id, errors = user.errors)

#this is to render a form for upload users avatar
@edits_blueprint.route('/photo_form')
@login_required
def profile_pic():
    return render_template('edits/profileimage.html')


#for allowed_file function, already transfer it to helpers.py
""" def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS """

#this is to upload file to S3, already transfer it to helpers.py
""" def upload_file_to_s3(file, bucket_name,acl='public-read'):
    try:
        s3.upload_fileobj(
            file, 
            bucket_name,
            file.filename,
            ExtraArgs={
                'ACL': acl, 
                'ContentType': file.content_type
            }
        )
    except Exception as e: 
        print('Something happened: ',e)
        return e
    
    return "{}{}".format(DevelopmentConfig.S3_LOCATION, file.filename) #app.config["S3_LOCATION"] """



#this is to return a string output after check file then upload file to S3
@edits_blueprint.route('/photo_form', methods = ['POST'])
@login_required
def upload_file():
    
    """ request.files['user_file'] # return <FileStorage: 'pokemon.jpg' ('image/jpeg')>
    request.files['user_file'].filename # return pokemon.jpg
    allowed = allowed_file(filename) # return True
    dev = DevelopmentConfig.S3_BUCKET

    return render_template('home.html', dev = dev) """

    if 'user_file' not in request.files: 
        return 'No user_file key in request.files'

    file = request.files['user_file']  

    if file.filename == '':
        return 'Please select a file'
    
    if file:
        #upload to the database
        user = User.get_by_id(current_user.id)
        user.profile_image = file.filename # should save pokemon.jpg

        #upload to s3
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file, DevelopmentConfig.S3_BUCKET)

        #if upload succesfully to both s3 and DB
        if user.save() and str(output): # return http://nextagramhang.s3.amazonaws.com/pokemon.jpg
            flash('You have uploaded photo succesfully','success')
            return redirect(url_for('users.show', username = user.name))
        else: 
            flash('Your photo is not uploaded', 'danger')
            return redirect(url_for('users/edit.upload_file'))
    else: 
        return redirect('/')




    









     








