from setuptools import setup,find_packages

from biocores.__version__ import __version__

with open('readme.md', 'r') as f:
    long_description = f.read()

tests_require = ['pytest']

setup(
    name='bioinfocore',
    version=__version__,
    packages=find_packages(),
    tests_require=tests_require,
    url='https://github.com/btrspg/bioinfo-core',
    license='GPL3License',
    author='Chen Yuelong',
    author_email='yuelong.chen.btr@gmail.com',
    description='Bioinformatics analysis cores',
    long_description=long_description
)
