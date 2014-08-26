from setuptools import setup

setup(
    name='Excerpts',
    version='0.0.0',
    author='aressler38',
    description='Write stuff to a DB',
    packages=['excerpts'],
    install_requires=[
        'Flask == 0.10.1',
        'MySQL-python == 1.2.3',
        'PyMySQL == 0.6.2'
    ]
)
