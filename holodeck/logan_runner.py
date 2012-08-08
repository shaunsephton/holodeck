import os
from logan.runner import run_app

CONFIG_TEMPLATE = """
import os.path
CONF_ROOT = os.path.dirname(__file__)

DATABASES = {
    'default': {
        # You can swap out the engine for MySQL easily by changing this value
        # to ``django.db.backends.mysql`` or to PostgreSQL with
        # ``django.db.backends.postgresql_psycopg2``
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(CONF_ROOT, 'holodeck.db'),
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Set this to False to require authentication
PUBLIC = False
"""

def generate_settings():
    """
    This command is run when ``default_path`` doesn't exist, or ``init`` is
    run and returns a string representing the default data to put into their
    settings file.
    """
    return CONFIG_TEMPLATE

def main():
    run_app(
        project='holodeck',
        default_config_path=os.path.join(os.getcwd(), 'holodeck.conf.py'),
        default_settings='holodeck.conf.defaults',
        settings_initializer=generate_settings,
        settings_envvar='HOLODECK_CONF',
    )

if __name__ == '__main__':
    main()
