from flask import Blueprint, render_template, flash, request,redirect, url_for
from models.user import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required, current_user


sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')

#this is to show the log in form
@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/login.html')

# this is to check new user inforamtion
@sessions_blueprint.route('/', methods=['GET','POST'])
def check():
    if request.method == 'POST':
    
        password_to_check = request.form['password']
        name = request.form['name']
        email = request.form['email']


        existing_name = User.get_or_none(User.name == name) # return True means already exsting 
        existing_email = User.get_or_none(User.email == email) # return True means already existing

        if existing_email and existing_name: 

            #get the user from the DB
            user_list = User.select().where(User.name == name)
            user = user_list[0]

            #check password
            hashed_password = user.password
            result_password = check_password_hash(hashed_password, password_to_check)

            if result_password:
                flash('You have login succesfully', 'success')
                #tell the browser to store the id for the session
                login_user(user)
                #return the homepage
                return render_template('home.html')
            else: 
                flash('Please try to log in again!', 'danger')
                return render_template('sessions/login.html')
        else:
            flash('Please try to log in again!', 'danger')
            return render_template('sessions/login.html')

    else: 
        return render_template('sessions/login.html')



@sessions_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    if current_user.is_authenticated is not True:
        flash('You have been log out succesfully', 'success')       
        return render_template('home.html')
    else: 
        flash('Log out again !!!', 'danger') 
        return render_template('home.html')
          
    


