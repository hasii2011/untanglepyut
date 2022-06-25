import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="untanglepyut",
    version="0.1.0",
    author_email='Humberto.A.Sanchez.II@gmail.com',
    description='XML to Ogl Object Model',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hasii2011/untanglepyut",
    packages=[
        'untanglepyut'
    ],
    install_requires=['ogl', 'untangle'],
)
