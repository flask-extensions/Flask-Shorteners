# coding: utf8

from setuptools import setup

setup(
    name='Flask-Shorteners',
    version='0.1',
    license='MIT',
    description='Flask Extension for some popular shorteners',
    long_description=open('README.md').read(),
    author=u'Ellison Leão',
    author_email='ellisonleao@gmail.com',
    url='https://github.com/ellisonleao/Flask-Shorteners/',
    platforms='any',
    zip_save=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],

    install_requires=['Flask', 'requests'],

    packages=['flaskext'],
    namespace_packages=['flaskext'],
)
