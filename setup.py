from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

install_requires = ['prompt-toolkit', 'google-api-python-client', 'google-auth-httplib2', 'google-auth-oauthlib']

setup(
    name='pyoklock',
    version='0.0.6',
    description='python cli digital clock.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/6syun9/pyoklock',
    license='MIT',
    author='vaaaaanquish',
    author_email='6syun9@gmail.com',
    install_requires=install_requires,
    packages=['pyoklock'],
    package_dir={'pyoklock': 'pyoklock'},
    package_data={'pyoklock': ['pyoklock/*']},
    entry_points={"console_scripts": ["pyoklock = pyoklock.main:main"]},
    platforms='any',
)
