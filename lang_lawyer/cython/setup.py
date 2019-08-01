from setuptools import setup
from Cython.Build import cythonize

# These hacks (with kwargs, see below) seem to not be required,
# when using setuptools.setup in lieu of distutils.core.setup
# Not that they helped anyway!
# Well, they did when doing this:
# import setuptools
# from distutils.core import setup
# (then setup_requires was placebo maybe?)
# Nevermind, I don't like unused imports anyway.
# kwargs = {}

try:
    import wheel
#     kwargs['setup_requires'] = ['wheel']
except ImportError:
    print('Missing wheel support')

setup(
    name='cython_hello',
    version='1.1',
    ext_modules = cythonize("hello.pyx")
    #, **kwargs
)
