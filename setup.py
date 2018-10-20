from setuptools import setup


setup(
    name='upfilter',
    version='0.1',
    author='Emma Hatton-Ellis',
    author_email='ehattonellis@gmail.com',
    description="Command-line utility for filtering UniProt fasta sequences.",
    python_requires='>=3',
    entry_points={
        'console_scripts': [
            'upfilter = upfilter.cli:main'
        ]
    }
)
