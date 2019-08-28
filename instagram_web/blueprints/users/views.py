from flask import Blueprint, render_template, flash, request,redirect, url_for

from models.user import User

from werkzeug.security import check_password_hash

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')

#this is to show the sign up form
@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')

# this is to take in new user inforamtion to the database
@users_blueprint.route('/', methods=['POST'])
def create():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    new_user = User(name=name, email=email, password = password)

    if new_user.save():
        flash('User has been created successfully','success')
        return redirect(url_for('users.new'))
    else: 
        flash('Please try again!','danger')
        return render_template('users/new.html' , errors = new_user.errors)


@users_blueprint.route('/', methods=["GET"])
def index():
    pass

@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass





@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
