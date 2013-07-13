from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()


version = '0.0.0'

install_requires = [
    # List your project dependencies here.
    # For more details, see:
    # http://packages.python.org/distribute/setuptools.html#declaring-dependencies
]


setup(name='django-cpe',
    version=version,
    description="Django implementation of CPE dictionary.",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='CPE Django',
    author='Alejandro Galindo Garc\xc3\xada, Roberto Abdelkader Mart\xc3\xadnez P\xc3\xa9rez',
    author_email='galindo.garcia.alejandro@gmail.com',
    url='',
    license='GPL3',
    packages=find_packages('src'),
    package_dir = {'': 'src'},include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'console_scripts':
            ['django-cpe=djangocpe:main']
    }
)
