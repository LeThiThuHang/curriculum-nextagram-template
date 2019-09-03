from models.base_model import BaseModel
import peewee as pw
from models.user import User

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property

import os

""" S3_DOMAIN = 'http://nextagramhang.s3.amazonaws.com/' """

class Image(BaseModel):
    user = pw.ForeignKeyField(User, backref='images')
    image_path = pw.CharField(null=True)


    @hybrid_property
    def image_url(self):
        return os.environ.get("S3_DOMAIN") + self.image_path

    def validate(self):
        return self.errors