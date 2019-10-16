from flask import Blueprint, render_template, flash, request,redirect, url_for
from models.user import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from app import oauth


sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')


#----------------------------------------LOG IN NORMALLY -----------------------------------------------------

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
                #return their own page
                return redirect(url_for('users.show', username = current_user.name))
            else: 
                flash('Please try to log in again!', 'danger')
                return render_template('sessions/login.html')
        else:
            flash('Please try to log in again!', 'danger')
            return render_template('sessions/login.html')

    else: 
        return render_template('sessions/login.html')

#----------------------------------------LOG OUT -----------------------------------------------------
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

#----------------------------------------LOG IN WITH GOOGLE -----------------------------------------------------
""" users is redirect after authenticate with Google
	https://localhost:5000/sessions/authorize/google
    For use with requests from a web server. 
    This is the path in your application that users are redirected to after they have authenticated with Google. 
    The path will be appended with the authorization code for access. 
    Must have a protocol. 
    Cannot contain URL fragments or relative paths. 
    Cannot be a public IP address. """

    
""" @sessions_blueprint.route('/login')
def login_google():
    #redirect to 3rd party: Google for authentication
    redirect_uri = url_for('authorize') """

@sessions_blueprint.route('/google_login')
def login():
    redirect_uri = url_for('sessions.authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)
    # 1. oauth.google.authorize_redirect
    # goes to google login page
    # 2. after logging in request will then be redirected to 'redirect_uri', get the code in the uri
    # 3. start the function authorize
    
@sessions_blueprint.route('/authorize/google')
def authorize():
    # do 2 things. return the auth code to Google and return the access token   
    token = oauth.google.authorize_access_token()
    #{'access_token': 'ya29.Glt5B0-IiPQSoIYp4ttqDZDbyN4mpjNX3tvYG-aOJDkyPrFFmkIRfZ0mNuaWO6EoCCwaiZOn72Mf_fT5X0tTxJVdHnhO4_H-a40lnn9CVSbSnoiTBeyF4kdk9AAJ', 
    #'expires_in': 3600, 
    #'scope': 'https://www.googleapis.com/auth/userinfo.email openid', 
    #'token_type': 'Bearer', 
    #'id_token': 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImY2ZjgwZjM3ZjIxYzIzZTYxZjJiZTQyMzFlMjdkMjY5ZDY2OTUzMjkiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiYXpwIjoiNzU4ODI1MTEyOTUxLWFiamN2anBrdDZza3FyNnMwOWtjY2UwNzd0cGxpYWdjLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiNzU4ODI1MTEyOTUxLWFiamN2anBrdDZza3FyNnMwOWtjY2UwNzd0cGxpYWdjLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTEwOTkzNDI1MjUwODMxMzQwNTA4IiwiZW1haWwiOiJ0aHVoYW5nLmxpdEBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXRfaGFzaCI6Imdpcjc4MzYwbG5hbl9acExDSlN4QUEiLCJpYXQiOjE1Njc1ODE4MTAsImV4cCI6MTU2NzU4NTQxMH0.kocS5Rvy9wmMefCm-KMF_7fm988u8laHN9Uk51GyJzwXwzGrimQiq4WDmfmZ5XPcglYiK5x-bO_Zsb8uFabTfMFH_8U5wNmgP5rEODqXt2LeRgey6SJTuUIbxSJxCqZqj85urOh8eGqKVXixsxgSjnJQ_jKjIuhmFGPeLhFVP18m2ANZL356YqKHDnw8mayZdsPsbpivyp29BECxOyHi6SDcXPQB8lZWS1ABcG9M4UosP91BVqnIwfZ4Gw6P5CKDY5EUyNiRruPCOMdjKynbKoJxsER8lNTE_cfNdU6JbVOLqbRvUQbJ9s9msnth1vu1WY5sGj_DutOstzhHTroyGA', 'expires_at': 1567585410}
    email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']

    user = User.get_or_none(User.email == email)

    if user: 
        login_user(user)
        flash('You have log in succesfully','success')
        return redirect(url_for('users.show', username = user.name))
    else:
        flash('You have problem login','danger')
        return redirect(url_for('sessions.new'))
    




    


