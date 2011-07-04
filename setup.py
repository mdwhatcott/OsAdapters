from distutils.core import setup

setup(
    name='OsAdapters',
    author='Michael Whatcott',
    author_email='mdwhatcott@gmail.com',
    url='https://www.github.com/mdwhatcott/OsAdapters',
    version='0.1',
    license='The MIT License (MIT)',
    description='Nice abstractions over the file system and running commands.',
    long_description=open('README').read(),
    packages=['osadapt'],
)
