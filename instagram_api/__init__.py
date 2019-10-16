from app import app
from flask_cors import CORS
import os 
import boto3, botocore
from flask import request, flash, redirect

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

## API Routes ##
from instagram_api.blueprints.users.views import users_api_blueprint


app.register_blueprint(users_api_blueprint, url_prefix='/api/v1/users')

# server side to send the json file to the upload images part POST API in user.html
@app.route('/sign_s3/')
def sign_s3():

    S3_BUCKET = os.environ.get('S3_BUCKET')

    file_name = request.args.get('file_name')
    file_type = request.args.get('file_type')

    s3 = boto3.client('s3')

    presigned_post = s3.generate_presigned_post(
        Bucket = S3_BUCKET,
        Key = file_name,
        Fields = {"acl": "public-read", "Content-Type": file_type},
        Conditions = [
        {"acl": "public-read"},
        {"Content-Type": file_type}
        ],
        ExpiresIn = 3600
    )

    return json.dumps({
        "data": presigned_post,
        "url": "https://nextagramhang.s3-ap-southeast-1.amazonaws.com/${file_name}"
    })


