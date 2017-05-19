# -*- coding: utf-8 -*-
"""
This module contains the tool of Products.PFGMasterSelect
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.2'

long_description = (
    read('README.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('Products', 'PFGMasterSelect', 'README.txt')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    'Download\n'
    '********\n')

tests_require = ['zope.testing']

setup(name='Products.PFGMasterSelect',
      version=version,
      description="Plone Formgen Fields using Master Select Widgets",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ],
      keywords='Plone PloneFormGen MasterSelectWidget',
      author='Bernhard Pöttinger',
      author_email='bernhard.poettinger@tngtech.com',
      url='https://github.com/bpoettinger/Products.PFGMasterSelect',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        # -*- Extra requirements: -*-
                        'Products.MasterSelectWidget',
                        'Products.DataGridField',
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite='Products.PFGMasterSelect.tests.test_docs.test_suite',
      entry_points="""
      # -*- entry_points -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
