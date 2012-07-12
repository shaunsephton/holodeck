from setuptools import setup, find_packages

setup(
    name='bitpile',
    version='0.0.1',
    description='Massively scalable datapoint storage app with plugable collectors.',
    long_description = open('README.rst', 'r').read() + open('AUTHORS.rst', 'r').read() + open('CHANGELOG.rst', 'r').read(),
    author='Shaun Sephton',
    author_email='shaun@28lines.com',
    url='http://github.com/shaunsephton/bitpile',
    packages = find_packages(),
    install_requires = [
        'django',
        'south',
    ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)
