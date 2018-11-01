#!/usr/bin/env python

from setuptools import setup, find_packages
import pkg_resources
import sys

setup(name='tex2word',
      version=open('VERSION').read().strip()
      ,description='Tool to convert latex documents to Microsoft Word'
      ,author='Adam Labadorf'
      ,author_email='alabadorf@gmail.com'
      ,install_requires=[
          'docopt',
          'future',
          'chardet',
          'bibtexparser',
          'docx',
          'pillow',
          'ply'
          ]
      ,packages=find_packages()
      ,entry_points={
        'console_scripts': [
          'tex2word=tex2word:main'
        ]
      }
      ,setup_requires=[
        'pytest-runner'
       ]
      ,tests_require=['pytest']
      ,url='https://github.com/adamlabadorf/tex2word/'
      ,license='MIT'
      ,classifiers=[
        'Development Status :: 3 - Alpha'
        ,'Environment :: Console'
        ,'License :: OSI Approved :: MIT License'
        ,'Programming Language :: Python :: 3'
      ]
      ,python_requires='~=3.3'
     )
