from setuptools import setup


with open('ecys.py') as source:
    ecys = {}
    for line in source.readlines():
        if line.startswith('__version__'):
            exec(line, ecys)
            break


README = open('README.rst').read()

setup(
    name='ecys',
    version=ecys['__version__'],
    py_modules=['ecys'],
    url='https://github.com/Djerys/ecys',
    license='MIT',
    author='Dmitry Kotukhov',
    author_email='djerys@ya.ru',
    description='A simple realization of Entity Component System',
    long_description=README
)
