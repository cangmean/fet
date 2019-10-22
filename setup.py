from setuptools import setup, find_packages

version = '0.1'
author = 'cangmean'

setup(
    name="fet",
    version=version,
    packages=find_packages(),
    include_package_data=True,
    author=author,
    url='https://github.com/cangmean/fet',
    install_requires=[
        'oss2', 'pytest', 'pycryptodome', 'redis', 'flask', 'flask-restful',
    ],
)
