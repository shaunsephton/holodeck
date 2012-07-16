from setuptools import setup, find_packages

setup(
    name='holodeck',
    version='0.0.4',
    description='Simple & scalable dashboard system.',
    long_description = open('README.rst', 'r').read() + open('AUTHORS.rst', 'r').read() + open('CHANGELOG.rst', 'r').read(),
    author='Praekelt Foundation',
    author_email='dev@praekelt.com',
    url='http://github.com/praekelt/holodeck',
    packages = find_packages(),
    install_requires = [
        'django',
        'south',
    ],
    include_package_data=True,
    scripts = ['holodeck/bin/holodeck'],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)
