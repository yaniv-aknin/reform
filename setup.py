"""
Reform
------

A utility to parse and reformat textual data files
"""
from setuptools import setup

setup(
    name='reform',
    version='0.1',
    license='BSD',
    author='Yaniv Aknin',
    author_email='yaniv@aknin.name',
    description='A utility to parse and reformat textual data files',
    long_description=__doc__,
    packages=['reform'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'reform = reform.main:baremain',
        ],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Development Status :: 4 - Beta'
    ]
)
