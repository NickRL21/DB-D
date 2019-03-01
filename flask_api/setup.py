# -*- encoding: utf-8 -*-
import io
import re
from os.path import dirname
from os.path import join

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ).read()


setup(
    name="dbd_api",
    version="0.1.0",
    license="Other/Proprietary License",
    description="api for db-d application",
    long_description="",
    author="Nicholas Lewis, Cody, Ardalan, Zi",
    author_email="",
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    url="",
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: Other/Proprietary License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.6"
        "Topic :: Utilities",
    ],
    install_requires=[
        "psycopg2",
        "flask",
        "flask_restful",
        "flask_api",
        "zappa"

    ],
    setup_requires=[]
)
