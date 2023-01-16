import setuptools
from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='StressModellingPackageTest',
  version='0.0.55',
  description=' ',
  long_description=open('README.txt').read(),
  url           = '',  
  author        = 'Sowmith Nandan',
  author_email  = 'sowmith.nandan@iiit.ac.in',
  license       = 'MIT', 
  classifiers   = classifiers,
  keywords      = 'Stress Modelling', 
  packages      = ['StressModellingPackageTest'],
  package_dir   = {'StressModellingPackageTest':'StressModellingPackageTest'},
  package_data  = {'StressModellingPackageTest':['data/*','data/PreComputedGraphs/*']},
  install_requires=[''] 
)