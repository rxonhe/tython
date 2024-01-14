import sys

from setuptools import setup, find_packages

VERSION = "0.0.5"

with open("README.md", "r") as fh:
    readme = fh.read()
    fh.close()

if sys.version_info.major != 3 and sys.version_info.minor < 10:
    sys.exit("'Tython' requires Python >= 3.10!")

setup(
    name="tython-toolkit",
    version=VERSION,
    packages=find_packages(),
    url="https://github.com/rxonhe/tython",
    license="MIT",
    author="Rafael Choinhet",
    author_email="choinhet@gmail.com",
    description="Tython goal is to implement cool features from other languages such as Kotlin, into Python.",
    long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    include_package_data=True,
    package_data={"": ["*.ttf", "*.png", "*.pdf", "*.jar", "*.json", "*.ini"]}

)
