from setuptools import setup
from setuptools import find_packages
import sys
import os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()


VERSION = '0.0.0'
AUTHORS = 'Alejandro Galindo Garc\xc3\xada, Roberto Abdelkader Mart\xc3\xadnez P\xc3\xa9rez'
EMAILS = 'galindo.garcia.alejandro@gmail.com, robertomartinezp@gmail.com'

install_requires = [
    'cpe',
]


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
      keywords='cpe django dictionary identification naming standard specification mitre nist',
      author=AUTHORS,
      author_email=EMAILS,
      maintainer='Alejandro Galindo Garc\xc3\xada',
      maintainer_email='galindo.garcia.alejandro@gmail.com',
      url='https://github.com/galindale/django-cpe',
      license='GPL3',
      packages=find_packages('src'),
      package_dir={'': 'src'}, include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      entry_points={
          'console_scripts':
              ['django-cpe=djangocpe:main']
          }
      )
