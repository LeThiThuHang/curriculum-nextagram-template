from flask import Blueprint, render_template, flash, request,redirect, url_for

from models.user import User
from models.image import Image
from models.payment import Payment

from werkzeug.security import check_password_hash

from flask_login import login_required, current_user

from helpers import s3, DevelopmentConfig, upload_file_to_s3, gateway, sending_email
from werkzeug.utils import secure_filename




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


#----------------------------------------SHOW USERS PROFILE PAGE-----------------------------------------------------

#this is to show the each profile page
@users_blueprint.route('/<username>', methods=["GET"])
@login_required
def show(username):
      
    user = User.get_or_none(User.name == username) 

    return render_template('users/user.html', user = user)

#----------------------------------------UPLOAD TO S3-----------------------------------------------------

#upload image to S3 and to the table Image
@users_blueprint.route('/<username>/images/upload', methods=['POST'])
@login_required
def image_upload(username):
    
    if 'user_file' not in request.files: 
        flash('Please choose file','danger')
        return redirect(url_for('users.show', username = current_user.name))

    file = request.files['user_file']  

    if file.filename == '':
        
        return flash('Please select a file','danger')
    
    if file:
        #upload to the database, table image
        image = Image.create(user_id = current_user.id, image_path = file.filename) 

        #upload to s3
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file, DevelopmentConfig.S3_BUCKET) # return the str(output)

        #if upload succesfully to both s3 and DB
        if image.save() and str(output): # return http://nextagramhang.s3.amazonaws.com/pokemon.jpg
           
            flash('You have uploaded photo succesfully','success')
            return redirect(url_for('users.show', username = current_user.name))
        else: 
            flash('Your photo is not uploaded', 'danger')
            return redirect(url_for('users/edit.upload_file'))
    else: 

        return redirect('/')

#----------------------------------------PAYMENT-----------------------------------------------------

# to render a payment form with username, image id and client token
@users_blueprint.route('/<username>/<imageid>/payment/new', methods=['POST'])
def checkout_new(username,imageid):
    client_token = gateway.client_token.generate()
    return render_template('users/payment.html', username = username, image_id = imageid, client_token = client_token)



# to show the check out result: no need this one
""" @users_blueprint.route('/<username>/checkouts/<transaction_id>', methods=['GET'])
def show_checkout(username,transaction_id):
    transaction = find_transaction(transaction_id)
    result = {}
    if transaction.status in TRANSACTION_SUCCESS_STATUSES:
        result = {
            'header': 'Sweet Success!',
            'icon': 'success',
            'message': 'Your test transaction has been successfully processed. See the Braintree API response and try again.'
        }
    else:
        result = {
            'header': 'Transaction Failed',
            'icon': 'fail',
            'message': 'Your test transaction has a status of ' + transaction.status + '. See the Braintree API response and try again.'
        }

    return render_template('users/checkout_result.html', transaction=transaction, result=result)
 """

# to submit check out to Braintree,
@users_blueprint.route('/<username>/checkout', methods=["POST"])
def create_checkout(username):
    amount = request.form['amount']
    image_id = request.form['image_id']

    result = gateway.transaction.sale({
        'amount': amount,
        #this one read the nonce from the form
        'payment_method_nonce': request.form['payment_method_nonce'], 
        'options': {
            'submit_for_settlement': True
        }
    })
    
    if result.is_success or result.transaction : 

        #update the money amount into the database Payment
        user = User.get_or_none(User.id == current_user.id)
        image = Image.get_by_id(image_id)
        payment = Payment(image = image,user = user, amount = amount)
        
        if payment.save():
            flash('You have donated succesfully','success')
            
            return redirect(url_for('users.thankyou', username = current_user.name))
            
        else: 
            flash('Can not save the new amount to database', 'danger')
            return redirect(url_for('users.checkout_new', username = current_user.name))
    else: 
        flash('Donate have problem','danger')
        for x in result.errors.deep_errors: flash('Error: %s: %s' % (x.code, x.message))
        return redirect(url_for('users.checkout_new', username = current_user.name))


#----------------------------------------SENDING OUT EMAIL-----------------------------------------------------

# to send the email after succesfully donate
@users_blueprint.route('/<username>/thankyou')
def thankyou(username):
    sending_email()

    return render_template('users/thankyou.html', username = username)



@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass



