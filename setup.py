from setuptools import setup, find_packages
#except ImportError:
#    from distutils.core import setup

setup(
    description = 'HomeseerPy',
    author = 'Manxam',
    author_email = 'manxam2k@hotmail.com',
    install_requires = ['lxml','requests','wsgiref', 'prettytable'],
    packages = find_packages(),
    version = '0.6',
    scripts = ['bin/hscontrol.py'],
    zip_safe = False,
    name = 'HomeseerPy',
)
