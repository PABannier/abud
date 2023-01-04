import os
from setuptools import setup, find_packages


version = None
with open(os.path.join('abud', '__init__.py'), 'r') as fid:
    for line in (line.strip() for line in fid):
        if line.startswith('__version__'):
            version = line.split('=')[1].strip().strip('\'')
            break
if version is None:
    raise RuntimeError('Could not determine version')

DISTNAME = 'abud'
DESCRIPTION = 'A lightweight pub-sub system for streaming data'
LICENSE = 'MIT'
DOWNLOAD_URL = 'https://github.com/PABannier/abud'
VERSION = version
URL = 'https://github.com/PABannier/abud'

setup(
    name=DISTNAME,
    version=version,
    description=DESCRIPTION,
    url=URL,
    download_url=DOWNLOAD_URL,
    packages=find_packages(),
)
