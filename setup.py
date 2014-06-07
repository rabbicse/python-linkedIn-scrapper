from distutils.core import setup
import py2exe

setup(
    windows=['Main.py'],
    options={"py2exe": {"includes": ["sip", "PyQt4.QtGui", "PyQt4.QtCore"]}},
    name='Nisbets',
    version='',
    packages=['spiders', 'logs', 'utils', 'works', 'views'],
    url='',
    license='',
    author='Rabbi',
    author_email='',
    description=''
)
