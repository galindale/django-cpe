#-*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages
import sys
import os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()


VERSION = u'0.0.0'
AUTHORS = u'Alejandro Galindo García, Roberto Abdelkader Martínez Pérez'
EMAILS = u'galindo.garcia.alejandro@gmail.com, robertomartinezp@gmail.com'

install_requires = [
    'django==1.4.9',
    # Request about API
    'requests==2.0.1',
    # API REST in Django
    'djangorestframework==2.3.9',
    # Parsing and validation of URIs (RFC 3986) and IRIs (RFC 3987)
    'rfc3987==1.3.2',
    # Migrations about models
    'south==0.8.4',
    'MySQL-python==1.2.4',
    # Generation and validation of CPE names
    'cpe',
]

dependency_links=[
    # Last release of pyiso8601 is not available on PyPI
    'https://bitbucket.org/micktwomey/pyiso8601/get/5b4f192e8077.zip',
],

setup(name='django-cpe',
      version=VERSION,
      description="Django implementation of CPE dictionary.",
      long_description=README + '\n\n' + NEWS,
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Framework :: Django",
          "Intended Audience :: Developers",
          "Intended Audience :: Information Technology",
          "Intended Audience :: System Administrators",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Natural Language :: English",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 2.7"],
      keywords=u'cpe django dictionary identification naming standard specification mitre nist',
      author=AUTHORS,
      author_email=EMAILS,
      maintainer=u'Alejandro Galindo García',
      maintainer_email=u'galindo.garcia.alejandro@gmail.com',
      url='https://github.com/galindale/django-cpe',
      license='GPL3',
      packages=find_packages('src'),
      package_dir={'': 'src'}, include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      #dependency_links=dependency_links,
      entry_points={
          'console_scripts':
              ['django-cpe=djangocpe:main']
      }
      )
