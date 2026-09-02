from setuptools import find_packages, setup

from paperlesspaper_client import __version__

with open("Readme.md") as f:
    long_description = f.read()

setup(
    name="paperlesspaper_client",
    version=__version__,
    author="infinityofspace",
    url="https://github.com/infinityofspace/paperlesspaper_client",
    description="Python client for the Paperlesspaper API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Utilities",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "setuptools~=84.0",
        "requests~=2.34",
    ],
    entry_points={
        "console_scripts": [
            "paperlesspaper = paperlesspaper_client.cli:main",
            "paperlesspaper-client = paperlesspaper_client.cli:main",
        ]
    },
)
