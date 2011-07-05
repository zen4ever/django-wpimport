#!/usr/bin/env python

from distutils.core import setup
import os

setup(name='django-wpimport',
      version='1.0',
      description='An utility app that helps you to create custom WordPress importer for your Django blog application.',
      author='Andrii Kurinnyi',
      author_email='andrew@zen4ever.com',
      url='https://github.com/zen4ever/django-wpimport',
      packages=['wpimport',],
      keywords=['django', 'wordpress', 'blogging',],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Programming Language :: Python',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Framework :: Django',
      ],
      long_description=open(
          os.path.join(os.path.dirname(__file__), 'README.rst'),
      ).read().strip(),
)
