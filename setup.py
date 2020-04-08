from setuptools import setup


README = open('README.rst').read()

setup(
    name='ecys',
    version='1.0.0',
    py_modules=['ecys'],
    url='https://github.com/Djerys/ecys',
    license='MIT',
    author='Dmitry Kotukhov',
    author_email='djerys@ya.ru',
    description='A simple realization of Entity Component System',
    long_description=README
)
