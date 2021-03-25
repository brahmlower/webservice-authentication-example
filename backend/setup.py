from setuptools import setup

setup(
    name = 'buildings_api',
    version = '0.1.0',
    description = 'An API about tall buildings',
    author = 'Brahm Lower',
    author_email = 'bplower@gmail.com',

    packages = ['buildings_api', 'buildings_api.domain', 'buildings_api.data_access'],
    package_dir = {'buildings_api': 'src'},
    install_requires = [
        'Flask==1.0.2',
        'PyYAML==5.4',
        'psycopg2-binary==2.7.7',
        'pyjwt==1.7.1',
        'flask-sqlalchemy==2.3.2',
        'google-auth==1.6.3',
        'requests==2.21.0',
        'bcrypt==3.1.6'
    ],
    entry_points = {
        'console_scripts': [
            'buildings-api=buildings_api:main'
        ]
    },
    classifiers = [
        "License :: OSI Approved :: MIT License"
    ]
)
