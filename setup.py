import setuptools
import re

with open('markov.py') as file:
    version = re.search(r"__version__ = '(.*)'", file.read())
    version = version.group(1)

with open('readme.md') as file:
    readme = file.read()

setuptools.setup(
    name='markov',
    description='Command line Markov chain text generator',
    long_description=readme,
    long_description_content_type='text/markdown',
    version=version,
    license='unlicense',
    py_modules=['markov'],
    entry_points={
        'console_scripts': [
            'markov = markov:main'
        ]
    },
    python_requires='~=3.8',
    classifiers=[
        'Environment :: Console',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: The Unlicense (Unlicense)'
    ]
)
