class BaseConfig(object):
    SQLALCHEMY_DATABASE_URI = (
        'mysql://jonathansaromo:'
        'jonathansdatabase'
        '@jonathansaromo.mysql.pythonanywhere-services.com/'
        'jonathansaromo$mysitedb')
    SQLALCHEMY_TRACK_MODIFICATIONS = False