#!/usr/bin/env python
"""This module contains setup instructions for iremover."""
import os
import codecs
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

with open(os.path.join(here, "iremover", "version.py")) as fp:
    exec(fp.read())

setup(
    name="iremover",
    version=__version__,  # noqa: F821
    author="Evgenii Pochechuev",
    author_email="ipchchv@gmail.com",
    packages=["iremover", ],
    package_data={"": ["LICENSE"], },
    url="https://github.com/pchchv/iremover",
    license="Apache-2.0 license",
    entry_points={
        "console_scripts": [
            "iremover = iremover.cli:main"], },
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    install_requires=[
        "aiohttp==3.8.4",
        "asyncer==0.0.2",
        "click==8.1.3",
        "fastapi==0.95.0",
        "numpy==1.24.2",
        "onnxruntime==1.14.1",
        "opencv-python==4.7.0.72",
        "opencv-python-headless==4.6.0.66",
        "pooch==1.6.0",
        "pymatting==1.1.8",
        "scipy==1.9.3",
        "tqdm==4.65.0",
        "uvicorn==0.21.1",
        "watchdog==3.0.0",
    ],
    description=("Python 3 library. Image background remover."),
    include_package_data=True,
    long_description_content_type="text/markdown",
    long_description=long_description,
    zip_safe=True,
    python_requires=">=3.7",
    project_urls={
        "Bug Reports": "https://github.com/pchchv/iremover/issues",
        "Read the Docs": "https://github.com/pchchv/iremover/docs",
    },
    keywords=["remove", "background",],
)
