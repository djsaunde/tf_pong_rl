from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

version = '0.1'

setup(
    name='pong',
    version=version,
    description='RL with Pong from the ground up.',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://github.com/djsaunde/pong',
    author='Daniel Saunders',
    author_email='danjsaund@gmail.com',
    packages=find_packages(),
    zip_safe=False,
    download_url='https://github.com/djsaunde/pong/archive/%s.tar.gz' % version,
)
