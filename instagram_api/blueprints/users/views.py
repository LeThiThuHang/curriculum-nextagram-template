from flask import Blueprint
from flask import jsonify
from flask_login import current_user
from models.user import User

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/me', methods=['GET'])
def get_current_user():
    if current_user:
        return jsonify(username=current_user.name,
                        email=current_user.email,
                        id=current_user.id)
    else: 
        return jsonify(username='',
                email='',
                id='')


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

#------------------------------API POST------------------------------------------------------------
#get request to take the current users login
@users_api_blueprint.route('/me', methods=['GET'])
def get_current_user(id):
    

    