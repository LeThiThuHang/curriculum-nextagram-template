from flask import Blueprint, jsonify, request, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_login import current_user
from models.user import User
from app import csrf

from helpers import upload_file_to_s3

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')


#----------------------------------------------------API GET-------------------------------------------------------------------------------------
#return the information of the users
@users_api_blueprint.route('/users', methods=['GET'])
def get_all_users():
    list=[{'username':user.name,'email':user.email,'id':user.id} for user in User.select()]
    return jsonify(list)

#return the information basing on id the users
@users_api_blueprint.route('/users/<id>', methods=['GET'])
def get_id_user(id):
    user = User.get_by_id(id)
    user_info={'username':user.name,'email':user.email,'id':id}
    return jsonify(user_info)

#return all images of the users
@users_api_blueprint.route('/images', methods=['GET'])
def get_all_images():
    users = User.select()
    list=[]
    for x in range(len(users)):
        user = users[x]
        list_each = {}

        list_each['user_id']=user.id
        list_each['user_name']=user.name
        list_each['user_email']=user.email
        list_each['profile_url']=user.profile_image_url
        list_each['images_url']=[]

        if len(user.images) > 0:
            
            for each in user.images:
                image_each={}
                image_each['image_id']=each.id
                image_each['images_url']=each.image_url
                list_each['images_url'].append(image_each)
        
        list.append(list_each)
        
    return jsonify(list)

#return all images of the user id
@users_api_blueprint.route('/images/<id>', methods=['GET'])
def get_user_image(id):
    user = User.get_by_id(id)
    list={}

    list['user_id']=user.id
    list['user_name']=user.name
    list['user_email']=user.email
    list['profile_url']=user.profile_image_url
    list['images_url']=[]
    
    if len(user.images) > 0:
        for each in user.images:
            image_each={}
            image_each['image_id']=each.id
            image_each['images_url']=each.image_url
            list['images_url'].append(image_each)
        
    return jsonify(list)

#------------------------------API GET AND POST WITH JWT------------------------------------------------------------
#get request to take the current users login

@users_api_blueprint.route('/login', methods=['POST'])
@csrf.exempt
def create_user():
    if not request.is_json:
        return jsonify({
            "msg":"Missing JSON"
        }), 400
    
    name = request.json.get('name')
    password = request.json.get('password')
    email = request.json.get('email')

    if not name: 
        return jsonify({
            "msg":"Missing JSON username parameter"
        }), 400

    if not password:
        return jsonify({
            "msg":"Missing JSON password parameter"
        }), 400
    
    if not email:
        return jsonify({
            "msg":"Missing JSON email parameter"
        }), 400
    
    user = User.create(
        name=name,
        password=password,
        email=email
    )

    if user.save():
        access_token = create_access_token(identity=user.id)
        return jsonify({
            "jwt":access_token
        }), 200
    else:
        return jsonify({user.errors}), 400 #bad request

#in Postman, put this shit in JSON
""" {
	"name":"john1",
	"password":"1A!1q112",
	"email":"johndoe1@gmail.com"
} """

""" it will return this shit: 
{
    "jwt": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1Njc4MzM1OTUsIm5iZiI6MTU2NzgzMzU5NSwianRpIjoiYTZiZTg0NjQtMTdkMi00MTQ2LWJlOWYtMTdiOTUzMzg1YjNkIiwiZXhwIjoxNTY3ODM0NDk1LCJpZGVudGl0eSI6NTEsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.M9cYmv1AGyL7X-SEeECDT5wBFE1_6iYuq0PJLt6iSgc"
}
 """

@users_api_blueprint.route('/me', methods=['GET'])
@jwt_required
def get_current_user():
    current_user_id = get_jwt_identity()
    
    current_user = User.get_by_id(current_user_id)

    return jsonify({
        "name":current_user.name,
        "email":current_user.email,
        "id":current_user.id
    })

""" it will return this shit: 
{ "email": "johndoe1@gmail.com", "id": 51, "name": "john1" } """

#------------------------------API POST IMAGES: method 1------------------------------------------------------------

#note: need to put the JWT token for security
@users_api_blueprint.route('/<userid>/image', methods=['POST'])
@csrf.exempt
def post_image(userid):
    """ # - files pass through your server, temporarily store in your server -> then get uploaded onto s3
    request.files -> AWS s3.upload -> get the url -> store in db -> return the url as json """
    image_file = request.files['user_file']
    
    upload_file_to_s3(image_file)
    
    #upload to the database
    user = User.get_by_id(userid)
    user.profile_image = image_file.filename
    
    if user.save():
        return jsonify({
            "name":user.name,
            "email":user.email,
            "image_url":user.profile_image_url
        })
    else: 
        return jsonify({user.errors}), 400 #bad request

#------------------------------API POST IMAGES: method 2------------------------------------------------------------
#render a template for submitting
@users_api_blueprint.route('/image/method2')
@csrf.exempt
def postAPI_image_form():
    return render_template('users_api/upload_images_api.html')

#return the Json file after submtting
@users_api_blueprint.route('/image/method2/post')
@csrf.exempt
def postAPI_image():
    profile_image_url = request.form["file_input"]

    user=User.get_by_id(51) #hard-coded for now

    user.image_url = profile_image_url

    if user.save():
        return jsonify({
            "name":user.name,
            "email":user.email,
            "profile_image_url":user.profile_image_url
        })
    else: 
        return jsonify({user.errors}), 400 #bad request

    