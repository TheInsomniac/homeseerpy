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
    scripts = [],
    zip_safe = False,
    name = 'HomeseerPy',
    entry_points = {
        'console_scripts':[
            'hscontrol = homeseerpy.hscontrol:main',
            ]
    }
)
