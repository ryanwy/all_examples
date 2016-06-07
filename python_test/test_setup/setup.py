from setuptools import setup, find_packages

setup(
    name = 'mycalc',
    version = '0.1',
    py_modules = ['mycalc'],
    entry_points = {
        'console_scripts': ['mycalc = mycalc:execute']
    },
)
