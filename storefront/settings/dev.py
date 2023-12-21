from .common import *

DEBUG = True

SECRET_KEY = 'django-insecure-$p_4poxw489=vtka@02vw&v_bikmppx2g+be+(nn^8cc!eg6*x'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'storefront',
        'HOST': 'localhost',
        'USER' : 'root',
        'PASSWORD' : '!@#alada123#',
        'PORT' : '3306',
        
    }
}