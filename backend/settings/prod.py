# -*-coding:utf-8 -*-
#
# Created on 2019/4/2, by felix
#

from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'stark',
        'USER': 'root',
        'PASSWORD': '111111',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
