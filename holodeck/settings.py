import os
import sys

PATH = os.path.split(os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]))))[0]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', 
        'NAME': os.path.join(PATH, 'holodeck.sqlite'),              
    }
}

PUBLIC = False
