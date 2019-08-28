from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

# for testing password 
import re 


class User(BaseModel, UserMixin):
    name = pw.CharField(unique=True) #unique, not allow null
    email = pw.CharField(unique=True, index=True) #index column, unique, not allow null
    password = pw.CharField() # no need to be unique

    def validate(self):
        duplicate_names = User.get_or_none(User.name == self.name)
        duplicate_emails = User.get_or_none(User.email == self.email)


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

