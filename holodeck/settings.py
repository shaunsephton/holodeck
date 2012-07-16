import os
import sys

PATH = os.path.split(os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]))))[0]

LOGICAL_SHARDS = 8

PHYSICAL_SHARDS = [
    {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME_PREFIX': os.path.join(PATH, 'holodeck_1'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
    {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME_PREFIX': os.path.join(PATH, 'holodeck_2'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
]

PUBLIC = False
