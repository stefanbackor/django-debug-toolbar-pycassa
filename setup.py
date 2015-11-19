from setuptools import setup, find_packages

setup(
    name='django-debug-toolbar-pycassa',
    version=":versiontools:debug_toolbar_pycassa:",
    description='Pycassa (Apache Cassandra) panel for the Django Debug Toolbar',
    long_description=open('README.md').read(),
    author='Stevo Backor',
    author_email='stevo@backor.sk',
    url='https://github.com/pista329/django-debug-toolbar-pycassa',
    license='MIT',
    packages=find_packages(), #exclude=('example', )
    include_package_data=True,
    zip_safe=False,
    setup_requires=[
        'versiontools >= 1.6',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)