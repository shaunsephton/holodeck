from setuptools import setup, find_packages

setup(
    name='holodeck',
    version='0.0.5',
    description='Simple & scalable dashboard system.',
    long_description = open('README.rst', 'r').read() + open('AUTHORS.rst', 'r').read() + open('CHANGELOG.rst', 'r').read(),
    author='Shaun Sephton',
    author_email='shaun@28lines.com',
    url='http://github.com/shaunsephton/holodeck',
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
