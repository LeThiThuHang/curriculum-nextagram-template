from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

#for hybrid
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property

# for testing password 
import re 

import os

""" S3_DOMAIN = 'http://nextagramhang.s3.amazonaws.com/' """


class User(BaseModel, UserMixin):
    
    name = pw.CharField(unique=True) #unique,
    email = pw.CharField(unique=True, index=True) #index column, 
    password = pw.CharField() # no need to be unique
    profile_image = pw.CharField(null=True)
    token = pw.CharField(null=True)

   
    @hybrid_property
    def profile_image_url(self):
        if self.profile_image is None: 
            return 'https://api.adorable.io/avatars/158/abott@adorable.png'
        else: 
            return os.environ.get("S3_DOMAIN") + self.profile_image

    def validate(self):
        duplicate_names = User.get_or_none(User.name == self.name)
        duplicate_emails = User.get_or_none(User.email == self.email)

        if not self.id: # only check for duplicate if users have not been log in
        # not self.id = True means self.id is false => means users have not been created
        #check for the email and username duplicate
            if duplicate_names: 
                self.errors.append('Name is not unique')
                
            if duplicate_emails:
                self.errors.append('Email is not unique')
        
            if len(self.password) < 6:
                self.errors.append('Password must be at least 6 characters')

            if re.search(r"[A-Z]", self.password) is None: 
                self.errors.append('Password must contains at least 1 upper case')
            
            if re.search(r"\d", self.password) is None: 
                self.errors.append('Password must contains at least 1 digit')
            
            if re.search(r"[!@$]", self.password) is None: 
                self.errors.append('Password must contains at least 1 symbol')
            else:
                self.password = generate_password_hash(self.password)
        

