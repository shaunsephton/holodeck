LOGICAL_SHARDS = 8

PHYSICAL_SHARDS = [
    {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME_PREFIX': 'holodeck1',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
    {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME_PREFIX': 'holodeck2',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
]
