import boto3, botocore
import braintree
from config import DevelopmentConfig

s3 = boto3.client(
    's3',
    aws_access_key_id=DevelopmentConfig.S3_KEY,
    aws_secret_access_key=DevelopmentConfig.S3_SECRET 
)


def upload_file_to_s3(file, bucket_name, acl="public-read"):

    try:

        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e
    
    return "{}{}".format(DevelopmentConfig.S3_LOCATION, file.filename)

#allowed_file


import braintree
import os

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=os.environ.get('BT_MERCHANT_ID'),
        public_key=os.environ.get('BT_PUBLIC_KEY'),
        private_key=os.environ.get('BT_PRIVATE_KEY')
    )
)

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def sending_email():
    message = Mail(
        from_email='thuhang.lit@gmail.com',
        to_emails='thuhang.lit@gmail.com',
        subject='Testing email with Sendgrid',
        html_content='<strong>Donation is received</strong>')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))

