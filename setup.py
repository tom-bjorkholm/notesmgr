#! /usr/local/bin/python3
"""Setup file specifying build of .whl."""

from setuptools import setup

setup(
  name='notesmgr',
  version='0.0.1',
  description='Manager for small notes and AI prompts.',
  author='Tom Björkholm',
  author_email='klausuler_linnet0q@icloud.com',
  python_requires='>=3.12',
  packages=['notesmgr'],
  package_dir={'notesmgr': 'src/notesmgr'},
  package_data={'notesmgr': ['py.typed']},
  entry_points={
    'gui_scripts': [
      'notesmgr=notesmgr.application:main'
    ]
  },
  install_requires=[
    'argcomplete >= 3.7.2',
    'edit-cfg-json-tk >= 0.3.0',
    'edit-cfg-json >= 0.3.0',
    'config-as-json >= 1.7',
    'packaging >= 26.3',
    'versionreporter >= 0.4'
  ]
)
