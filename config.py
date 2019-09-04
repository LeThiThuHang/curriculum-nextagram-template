import os



class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or os.urandom(32)
    
    client_id=os.environ.get("GOOGLE_CLIENT_ID")
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET")


class ProductionConfig(Config):
    DEBUG = False
    ASSETS_DEBUG = False
    


class StagingConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    ASSETS_DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    ASSETS_DEBUG = False

    S3_BUCKET                 = os.environ.get("S3_BUCKET")
    S3_KEY                    = os.environ.get("S3_KEY")
    S3_SECRET                 = os.environ.get("S3_SECRET_ACCESS_KEY")
    S3_LOCATION               = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

    DEBUG                     = True
    PORT                      = 5000
    
    #for Google authorization



class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    ASSETS_DEBUG = True





