from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_login import current_user
from models.user import User
from app import csrf

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

#------------------------------API GET WITH JWT------------------------------------------------------------
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

    

    