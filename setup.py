from setuptools import setup

setup(
    name="sieve",
    version="1.0.0",
    url="https://github.com/ehatton/sieve",
    author="Emma Hatton-Ellis",
    author_email="ehattonellis@gmail.com",
    license="MIT",
    packages=["sieve"],
    install_requires=["click"],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["sieve=sieve.cli:main"]},
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    zip_safe=False,
)
