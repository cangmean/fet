from setuptools import setup, find_packages
import fet

version = fet.__version__
author = fet.__author__

setup(
    name="fet",
    version=version,
    packages=find_packages(),
    include_package_data=True,
    author=author,
    url='https://github.com/cangmean/fet',
    install_requires=[
        'oss2', 'pytest', 'pycryptodome'
    ],
)