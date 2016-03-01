from setuptools import setup, find_packages

with open('./README.rst', 'rb') as f:
    description = f.read()

setup(
    name='myweb',
    description='My Web Framework And HTTP Proxy.',
    long_description=description,
    version='0.1',
    author='jiaju.chen',
    author_email='importcjj@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/importcjj/myweb.py'
)
