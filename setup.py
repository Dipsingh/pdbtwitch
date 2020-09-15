from distutils.core import setup
from setuptools import find_packages
import os

setup(
    name="peeringdb",
    version=os.environ.get("PKG_VERSION", None),
    python_requires='>=3.6',
    packages=find_packages(),
    description="library for pulling peeringdb info",
    author="xyz@xyz.com",
    install_requires=[
        'bokeh>=2.1.1',
        'pandas>=0.25.2'
    ],
    url='https://xyz.com',
    include_package_data=True,
    data_files=[
        ('notebooks', ['notebooks/peeringdb.ipynb'])
    ]
)
