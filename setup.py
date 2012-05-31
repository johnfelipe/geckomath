from distutils.core import setup
import os
import py2exe

dll_excludes=['w9xpopen.exe']

# gather all of the geckomodules
geckomodules = os.listdir('geckomodules')
geckomodules = [file for file in geckomodules
                if file.endswith('.py') and file != '__init__.py']
geckomodules = ['geckomodules.{}'.format(os.path.splitext(module)[0]) 
                for module in geckomodules]

setup(
    name='Geckomath',
    version='0.1',
    decription='Randomly generate math problems',
    author='John Dougherty',
    author_email='john.e.dougherty.ii@gmail.com',
    packages=['geckomodules'],
    options = {
        'py2exe': {
            'ascii': False, 
            'bundle_files': 1, 
            'compressed': 2, 
            'dll_excludes': dll_excludes, 
            'optimize': 2, 
            'packages': ['geckomodules'] + geckomodules,
            'xref': False, 
            'skip_archive': False, 
        },
    },
    zipfile = None,
    windows=[{
        'script': 'geckogui.py',
        'dest_base': 'geckomath',
        'icon_resources': [(0, 'icons/geckomath.ico')],
    }]
)
