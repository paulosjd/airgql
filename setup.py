import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

requires = [
    'plaster_pastedeploy',
    'pyramid',
    'pyramid_mako',
    'pyramid_debugtoolbar',
    'waitress',
    'alembic',
    'pyramid_retry',
    'pyramid_tm',
    'psycopg2',
    'bs4',
    'lxml',
    'pytz',
    'requests',
    'Celery',
    'redis',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
]

tests_require = [
    'WebTest >= 1.3.1',
    'pytest >= 3.7.4',
    'pytest-cov',
]

setup(
    name='airgql',
    version='1.2',
    description='airgql',
    long_description=README,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='',
    author_email='',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
    },
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = airgql:main',
        ],
        'console_scripts': [
            'initialize_airgql_db=airgql.scripts.initialize_db:main',
            'aurn_hourly_create=airgql.scripts.aurn_hourly_create:main',
        ],
    },
)
