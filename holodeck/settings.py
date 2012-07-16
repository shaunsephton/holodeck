LOGICAL_SHARDS = 8

PHYSICAL_SHARDS = [
    {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME_PREFIX': 'holodeck_1',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
    {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME_PREFIX': 'holodeck_2',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
]

PUBLIC = False
