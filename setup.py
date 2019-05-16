from setuptools import setup, find_packages

requires = [
    'flask',
    'flask-sqlalchemy',
    'psycopg2',
]

setup(
    name='flask_todo',
    version='1.0',
    description='Deep Code Web UI',
    author='Vinoj Jayasundara',
    author_email='vinojjayasundara@gmail.com',
    keywords='web flask',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)