import setuptools
import re

with open('markov.py', 'r') as file:
    version = re.search(r"__version__ = '(.*)'", file.read())
    version = version.group(1)

setuptools.setup(
    name='markov',
    version=version,
    py_modules=['markov'],
    entry_points={
        'console_scripts': [
            'markov = markov:main'
        ]
    },
    python_requires='~=3.8'
)
